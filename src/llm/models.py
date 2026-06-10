import os
from dotenv import load_dotenv
from mistralai.client import Mistral
from src.llm.tools import main_assistant_tools

load_dotenv()

main_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
validation_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))

def mistral_model_parameters():
    model_parameters = {
    "temperature": 0.7,
    "max_tokens": 2048,
    "top_p": 1,
    "model": "mistral-medium-latest"
}
    return model_parameters
def main_client(client_message):
    client_response = main_client.chat.complete(
    **mistral_model_parameters(),
            messages= client_message,
            tools = main_assistant_tools
        )
    return(client_response)

def validation_client(validate_message):
    validation_response = validation_client.chat.complete(
    **mistral_model_parameters(),
            messages= validate_message
        )
    return(validation_response)
