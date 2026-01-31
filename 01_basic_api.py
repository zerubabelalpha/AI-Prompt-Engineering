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

# load environment variable
load_dotenv()

# Configure the model

def setup_model():

    api_key=os.getenv("API_KEY")

    if not api_key:
        print("please setup api key inside .env")
        return
    
    client = OpenAI(
                    base_url = "https://openrouter.ai/api/v1",
                    api_key = api_key,
                    )
    return client



def simple_chat(client, prompt,model_name="arcee-ai/trinity-mini:free"):

    try:
        response =  client.responses.create(
        model=model_name,
        input=prompt
        )

        reply = response.output_text
        
        #print("AI :",reply)

        md=Markdown(reply)
        console.print(md)
        print()

        return reply



    except Exception as e:
        print ("error occured",e)
        return


if __name__=="__main__":
    print("==== Model Testing ====")

    client = setup_model()
    if not client:
        exit(1)


    while True:
        user_input = input("Ask me anything...  (quit) to exit.\n")
        if user_input.lower()=='quit':
            break
        simple_chat(client, user_input)