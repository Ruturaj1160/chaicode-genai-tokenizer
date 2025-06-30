import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

# Load environment variables from a .env file
load_dotenv()

# Define a function to retrieve counterparty information based on ID

def get_counterparty(counterpartyId: str):
    print(f" 🛠️: Tool called with counterparty ID: {counterpartyId}")

    # Simulate a delay to mimic async behavior
    time.sleep(0.5)

    # Mock data representing counterparty information
    counterpartyData = [
        {"counterpartyId": "123", "name": "Counterparty 123", "status": "active"},
        {"counterpartyId": "456", "name": "Counterparty 456", "status": "inactive"},
        {"counterpartyId": "789", "name": "Counterparty 789", "status": "active"}
    ]

    # Search for the counterparty matching the given ID
    for counterparty in counterpartyData:
        if counterparty["counterpartyId"] == counterpartyId:
            print(f" 🛠️: found match {counterpartyId}")
            return counterparty


# Define available tools and their descriptions
available_tools = {
    "get_counterparty": {
        "fn": get_counterparty,
        "description": "Takes a counterparty ID as input and returns information about the counterparty"
    },
}

try:
    # Initialize the OpenAI client with API key and base URL
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Define the system prompt for the AI assistant
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
        - get_counterparty: Takes a counterparty ID as input and returns information about the counterparty

    Example:
    User Query: Give me status of counterparty 123?
    Output: {{ "step": "plan",
        "content":"The user is interested in the status of counterparty 123."}}
    Output: {{ "step":"plan",
        "content":"I will use the get_counterparty tool to get the status of counterparty 123."}}
    Output: {{ "step":"action", "function":"get_counterparty", "input":"123"}}
    Output: {{ "step":"observe", "output": ("id": "123", "name": "Counterparty 123", "status": "active") }}
    Output:{{ "step":"output", "content":"The status of counterparty 123 is active."}}

    """

    # Initialize the conversation with the system prompt
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        # Get user input
        user_query = input('--> ')
        if user_query == "exit":
            break
        messages.append({"role": "user", "content": user_query})

        while True:
            # Send the conversation to the OpenAI API and get a response
            reponse = client.chat.completions.create(
                model="gemini-2.0-flash",  # Specify the model to use
                response_format={"type": "json_object"},
                messages=messages
            )

            # Parse the JSON response from the API
            parsed_output = json.loads(reponse.choices[0].message.content)
            messages.append(
                {"role": "assistant", "content": json.dumps(parsed_output)}
            )

            # Handle the "plan" step
            if parsed_output.get("step") == "plan":
                print(f"🧠 :{parsed_output.get('content')}")

            # Handle the "action" step
            if parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")

                print(f" 🛠️: Tool called with counterparty ID: {tool_name}")
                print(f" 🛠️: Tool called with counterparty ID: {tool_input}")

                # Execute the tool if it exists in available_tools
                if available_tools.get(tool_name, False):
                    output = available_tools[tool_name].get(
                        "fn")(str(tool_input))
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

            # Handle the "output" step
            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get('content')}")
                break

except Exception as e:
    # Catch and print any errors that occur during execution
    print(f" error in response : {e}")
