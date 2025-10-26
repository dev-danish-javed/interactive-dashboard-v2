from datetime import datetime
from google import genai
from google.genai import types
from google.genai.types import Content, Part, FunctionDeclaration, Schema, Type
from pydantic import BaseModel

from configurations.configs import get_chat_client_api_key

# --- Define function declarations ---
schedule_meeting_function = FunctionDeclaration(
    name="schedule_meeting",
    description="Schedules a meeting with specified attendees at a given time and date.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "attendees": Schema(type=Type.ARRAY, items=Schema(type=Type.STRING)),
            "date": Schema(type=Type.STRING, description="Date of the meeting (e.g., '2024-07-29')"),
            "time": Schema(type=Type.STRING, description="Time of the meeting (e.g., '15:00')"),
            "topic": Schema(type=Type.STRING, description="The subject or topic of the meeting."),
        },
        required=["attendees", "date", "time", "topic"]
    )
)

get_date_function_declaration = FunctionDeclaration(
    name="get_today_date",
    description="Returns today's date",
    parameters=Schema(type=Type.NULL)
)

# --- Map function names to Python functions ---
FUNCTION_MAP = {
    "schedule_meeting": lambda **args: schedule_meeting(**args),
    "get_today_date": lambda **args: get_today_date(),
}

# --- Structured response schema ---
class LLMResponseSchema(BaseModel):
    summary: str
    response: str
    next_steps: list[str]

# --- Setup client ---
client = genai.Client(api_key=get_chat_client_api_key())
tools = types.Tool(function_declarations=[schedule_meeting_function, get_date_function_declaration])

# --- Functions to execute ---
def schedule_meeting(attendees, date, time, topic):
    return {"summary": f"Meeting with {', '.join(attendees)} scheduled.", "next_steps": ["Send invites", "Prepare agenda"]}

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

# --- Chat history ---
chat = []

while True:
    user_input = input("User: ")

    if not user_input.strip():
        for content in chat:
            print('_'.center(50, '_'))
            print(f"{content.role}: \t\t{content.parts[0].text}")
        exit(0)

    chat.append(Content(role="user", parts=[Part(text=user_input)]))

    # Step 1: ask model with function declarations
    config_functions_only = types.GenerateContentConfig(tools=[tools])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=chat,
        config=config_functions_only
    )

    # Check if model wants to call a function
    function_call = response.candidates[0].content.parts[0].function_call
    if function_call:
        func_name = function_call.name
        func_args = function_call.args or {}

        if func_name in FUNCTION_MAP:
            function_result = FUNCTION_MAP[func_name](**func_args)

            # Append function result as model message
            chat.append(Content(
                role="model",
                parts=[Part(text=f"Function '{func_name}' executed. Result: {str(function_result)}")]
            ))

            print(f"\tFunction '{func_name}' executed. Result: {str(function_result)}")

            # Step 2: feed function result back to model to get structured output
            config_schema_only = types.GenerateContentConfig(response_schema=LLMResponseSchema, response_mime_type="application/json")
            structured_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=chat,
                config=config_schema_only
            )

            parsed = structured_response.parsed
            print(f"\tAssistant Summary: {parsed.summary}")
            print(f"\tNext Steps: {parsed.next_steps}")
            print(f"Assistant Response: {parsed.response}")
            chat.append(Content(role="model", parts=[Part(text=parsed.summary)]))
        else:
            print(f"No Python implementation found for function '{func_name}'")

    else:
        model_text = response.candidates[0].content.parts[0].text
        print(f"Assistant: {model_text}")
        chat.append(Content(role="model", parts=[Part(text=model_text)]))
