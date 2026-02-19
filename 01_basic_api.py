"""
*
* Testing ai model from openrouter 
* interact with the model inside terminal for query and rendered response
*
"""
from openai import OpenAI
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown


console = Console()

conversation_history =[]
PROMPT_TEMPLATE = """
Task:
{task}
if the task is releted to coding follow the instructions.
Instructions:
Assume you are proessional software engineer, which builds project in organied, simplified and consise way.
1. provide the idea in organized and structured way,
2. provide file structure
3. generate task and implementation plan for the project
4. implement the tasks according to the implementation plan that you provided.
5. write and provide a command for the test cases.
6. provide a setup.md file which help the user to understand and execute the project in his machine.
"""
# load environment variable
load_dotenv()

# Configure the model

def setup_model():

    API_KEY=os.getenv("API_KEY")

    if not API_KEY:
        print("please setup api key inside .env")
        return
    
    client = OpenAI(
                    base_url = "https://openrouter.ai/api/v1",
                    api_key = API_KEY,
                    )
    return client


def simple_chat(client, prompt,model_name="arcee-ai/trinity-large-preview:free"):

    try:
        response =  client.responses.create(
        model=model_name,
        input=prompt
        )

        reply = response.output_text or "_(No response)_"
        
        #print("AI :",reply)

        md=Markdown(reply)
        console.print(md)
        print()

        return reply

    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None


def generate_with_parameters(
        client,   
        temp, 
        max_token,
        template, 
        model_name="arcee-ai/trinity-large-preview:free",
        role="user",
        **kwargs
        ):

    try:

        try:
            prompt = template.format(**kwargs)
        except KeyError as e:
            console.print(f"[bold red]Template missing variable:[/bold red] {e}")
            return None
        conversation_history.append({
            'role':role,
            'content': prompt
        })

        MAX_HISTORY = 20
        if len(conversation_history) > MAX_HISTORY:
            conversation_history[:] = conversation_history[-MAX_HISTORY:]

        stream = client.responses.create(
            model=model_name,
            input=conversation_history,
            temperature = temp,
            max_output_tokens = max_token,
            stream=True
        )

        full_reply=""


        for event in stream:
            if event.type == "response.output_text.delta":
                delta = event.delta
                full_reply += delta
                print(delta, end="", flush=True)

        print("\n")
        
         # Save assistant reply to memory
        conversation_history.append({
            "role": role,
            "content": full_reply
        })
        return full_reply


    except Exception as e:
        console.print (f"[bold red]Error occurred:[/bold red] {e}")
        return None   



if __name__=="__main__":
    console.print("[bold cyan]==== Model Testing ==== [/bold cyan]\n")

    client = setup_model()
    if not client:
        exit(1)


    while True:
        user_input = input("Ask me anything...  (quit to exit).\n> ")
        if user_input.lower()=='quit':
            break
        #simple_chat(client, user_input)
        generate_with_parameters(
            client, 
            temp=0.7, 
            max_token=5000, 
            template=PROMPT_TEMPLATE, 
            role="developer", 
            task=user_input)

