from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(

    api_key=os.getenv("OPENROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1"

)


def chat(messages, model="meta-llama/llama-3.2-3b-instruct:free"):
    """
    Send messages to the model and return text.
    """

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content