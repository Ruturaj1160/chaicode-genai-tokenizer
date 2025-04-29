import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


def get_weather(city: str):
    print(f" 🛠️: Tool called", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"
        return 'Something went wrong'
    except requests.exceptions.SSLError as e:
        return f"SSL Error: {e}"


def run_command(command):
    result = os.system(command=command)
    return result


available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as input and returns the weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output"

    }
}


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
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input to the function if the step is action",
    }}

    Available Tools:
    - get_weather: Takes a city name as input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns output



    Example:
    User Query: What is the weather of New York?
    Output: {{ "step": "plan",
        "content":"The user is interested in weather data of new york."}}
    Output: {{ "step":"plan",
        "content":"I will use the weather API to get the weather data of new york."}}
    Output: {{ "step":"action", "function":"get_weather", "input":"New York"}}
    Output: {{ "step":"observe", "output": "12 degree celsius, sunny"}}
    Output:{{ "step":"output", "content":"The weather of New York is 12 degree celsius and sunny."}}

    """
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    while True:

        user_query = input('--> ')
        if user_query == "exit":
            break
        messages.append({"role": "user", "content": user_query})

        while True:

            reponse = client.chat.completions.create(
                model="gemini-2.0-flash",  # or "gemini-1.5-turbo-16k"
                response_format={"type": "json_object"},
                messages=messages
            )
            parsed_output = json.loads(reponse.choices[0].message.content)
            messages.append(
                {"role": "assistant", "content": json.dumps(parsed_output)})

            if parsed_output.get("step") == "plan":
                print(f"🧠 :{parsed_output.get('content')}")

            if parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")

                if available_tools.get(tool_name, False):
                    output = available_tools[tool_name].get("fn")(tool_input)
                    messages.append(
                        {
                            "role": "assistant",
                            "content": json.dumps({
                                "step": "observe",
                                "output": output
                            })
                        }
                    )
                    continue

            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                break


except Exception as e:
    print(f" error in response : {e}")
