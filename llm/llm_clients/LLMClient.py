from enum import Enum
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from humanfriendly.terminal import message
from pydantic import BaseModel

from configurations.configs import get_chat_client_api_key, get_chat_llm_model, get_embedding_model


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

class LLMNaturalLanguageResponseSchema(BaseModel):
    response: str
    invalid_request: bool = False

class LLMClient:
    def get_sql_command(self, chat, message):
        """Process messages with llm"""
        pass

    def prepare_response(self, chat, message):
        """Prepares a response for the user query in natural language"""
        pass

    def embed(self, content: str):
        """Embed messages with llm"""
        pass

    def get_chat_history(self, chat):
        """Get chat with given chat_id"""
        pass

    def create_chat(self, system_prompt:str):
        """Creates and intialize a new chat"""
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

    def create_chat(self, system_prompt=None):
        """Creates and intialize a new chat"""
        return [{"role":"system", "content": system_prompt}]

    def get_sql_command(self, chat, message):
        """Process messages with llm"""
        try:
            chat.append({"role": "user", "content": message})
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=str(chat),
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': LLMSQLResponseSchema,
                },
            )
            response = response.parsed
            return response.sql
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

    def prepare_response(self, chat, message):
        """Process messages with llm"""
        try:
            response = self.client.models.generate_content(
                model=self.chat_model,
                contents=message,

                config={
                    'response_mime_type': 'application/json',
                    'response_schema': LLMNaturalLanguageResponseSchema,
                },
            )
            response = response.parsed
            return response.response
        except Exception as error:
            print(error)


class OpenAIClient(LLMClient):
    pass