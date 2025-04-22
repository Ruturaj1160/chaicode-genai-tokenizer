from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are helpuy
"""

reponse = client.chat.completions.create(
    model="gemini-1.5-turbo", # or "gemini-1.5-turbo-16k"
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    temperature=0.7,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

print("Response:")
print(reponse.choices[0].message.content)