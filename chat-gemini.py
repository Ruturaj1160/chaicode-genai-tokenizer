from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

try:
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

    )

    system_prompt = """
    You are helpful AI assisttan who is specailised in resolving user query.
    You work on start, plan, action and observe mode.
    For the given user query and available tools, plan the step by step execution, based on planning, select the releavnt tool and 
    based on the tool selection you perform an action and action to call the tool. Wait for observation and based on the observation you will decide the next step.

    Rules:
    - Follow the output JSON format strictly.
    - Always perforom one step at a time and wait for next input
    - Carefully analyze the user query and plan the steps.

    Output JSON format:
    {{
    "Step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input to the function if the step is action",
    }}
    
    Example:
    User Query: What is the weather of New York?
    Output: {{ "step": "plan", "content":"The user is interested in weather data of new york."}}
    Output: {{ "step":"plan", "content":"I will use the weather API to get the weather data of new york."}}
    Output: {{ "step":"action", "function":"get_weather", "input":"New York"}}
    Output: {{ "step":"observe", "output": "12 degree celsius, sunny"}}
    Output:{{"output":"The weather of New York is 12 degree celsius and sunny."}}

    """

    reponse = client.chat.completions.create(
        model="gemini-2.0-flash",  # or "gemini-1.5-turbo-16k"
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
