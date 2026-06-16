from dotenv import load_dotenv
import os

from openai import OpenAI

# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv("OPENROUTER_MODEL", "nex-agi/nex-n2-pro:free")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def chat(
    messages,
    model=MODEL_NAME,
    response_format=None,
):
    """
    Send messages to the model and return text.
    """

    request_kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 0,
    }

    if response_format is not None:

        request_kwargs["response_format"] = response_format

    response = client.chat.completions.create(**request_kwargs)
    return response.choices[0].message.content