from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

try:
    client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    system_prompt = """
    You are helpfull
    """

    reponse = client.chat.completions.create(
        model="gemini-2.0-flash", # or "gemini-1.5-turbo-16k"
        messages=[
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
    )

    print("Response:")
    print(reponse.choices[0].message.content)
except Exception as e:
    print(f" error: {e}")