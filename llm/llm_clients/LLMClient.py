from enum import Enum
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, Content, Part
from humanfriendly.terminal import message
from pydantic import BaseModel

from configurations.configs import get_chat_client_api_key, get_chat_llm_model, get_embedding_model
from llm.llm_functions import execute_sql_query_function_declaration, LLM_FUNCTION_MAP, bar_chart_function


class LLMClients(Enum):
    # Enum members are defined as class variables
    GEMINI = 'GEMINI'
    OPENAI = 'OPENAI'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

class LLMSQLResponseSchema(BaseModel):
    sql: str
    invalid_request: bool = False

class LLMProcessDBResultResponseSchema(BaseModel):
    response: str
    invalid_request: bool = False
    can_create_chart_on_data: bool
    chart_type: str
    relevant_question_for_chart_data: str

class LLMClient:
    def get_query_data(self, chat, message) -> LLMSQLResponseSchema:
        """Process messages with llm"""
        pass

    def process_db_result(self, chat, message) -> LLMProcessDBResultResponseSchema:
        """Prepares a response for the user query in natural language"""
        pass

    def embed(self, content: str):
        """Embed messages with llm"""
        pass

    def get_chat_history(self, chat):
        """Get chat with given chat_id"""
        pass

    def create_chat(self, chart_prompt:str):
        """Creates and intialize a new chat"""
        pass

    def create_chart(self, chart_prompt:str):
        pass

class GeminiClient(LLMClient):

    _instance= None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = genai.Client(api_key= get_chat_client_api_key())
        return cls._instance


    def __init__(self):
        # self.client = genai.Client(api_key= get_chat_client_api_key())
        self.chat_model = get_chat_llm_model()
        self.embedding_model = get_embedding_model()

    def create_chat(self, chart_prompt=None):
        """Creates and intialize a new chat"""
        tools = types.Tool(function_declarations=[bar_chart_function])
        config_chart_functions_only = types.GenerateContentConfig(tools=[tools])
        response = self.client.models.generate_content(
            model=self.chat_model,
            contents=chart_prompt,
            config=config_chart_functions_only
        )

        function_call = response.candidates[0].content.parts[0].function_call

        if function_call:
            func_name = function_call.name
            func_args = function_call.args or {}

            if func_name in LLM_FUNCTION_MAP:
                function_result = LLM_FUNCTION_MAP[func_name](**func_args)
                return function_result
        return [{"role":"user", "content": chart_prompt}]

    def get_query_data(self, chat, message) -> LLMSQLResponseSchema:
        """Process messages with llm"""
        try:
            chat.append({"role": "user", "content": message})
            tools = types.Tool(function_declarations=[execute_sql_query_function_declaration])
            config_functions_only = types.GenerateContentConfig(tools=[tools])
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=str(chat),
                config=config_functions_only
            )

            function_call = response.candidates[0].content.parts[0].function_call

            if function_call:
                func_name = function_call.name
                func_args = function_call.args or {}

                if func_name in LLM_FUNCTION_MAP:
                    function_result = LLM_FUNCTION_MAP[func_name](**func_args)
                    chat.append(Content(
                        role="model",
                        parts=[Part(text=f"Function '{func_name}' executed. Result: {str(function_result)}")]
                    ))
                    return function_result

            return None
        except Exception as error:
            print(error)

    def get_chat_history(self, chat):
        return chat

    def embed(self, content: str):
        """Embed messages with llm"""
        result = self.client.models.embed_content(
            model=self.embedding_model,
            contents=content
        )
        return result.embeddings

    def process_db_result(self, chat, message) -> LLMProcessDBResultResponseSchema:
        """Process messages with llm"""
        try:
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=message,

                config={
                    'response_mime_type': 'application/json',
                    'response_schema': LLMProcessDBResultResponseSchema,
                },
            )
            response = response.parsed
            chat.append({"role":"assistant", "content": response.response})
            return response
        except Exception as error:
            print(error)

    

class OpenAIClient(LLMClient):
    pass