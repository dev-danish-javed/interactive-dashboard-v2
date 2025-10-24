from enum import Enum
from google import genai
from google.genai import types

from configurations.configs import get_chat_client_api_key, get_chat_llm_model, get_embedding_model


class LLMClients(Enum):
    # Enum members are defined as class variables
    GEMINI = 'GEMINI'
    OPENAI = 'OPENAI'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

class LLMClient:
    def ping(self, chat, message):
        """Process messages with llm"""
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
        return self.client.chats.create(model=self.chat_model,
                                        config= types.GenerateContentConfig(
                                            system_instruction= system_prompt))

    def ping(self, chat, message):
        """Process messages with llm"""
        try:
            response = chat.send_message(message)
            return response.text
        except Exception as error:
            print(error)

    def get_chat_history(self, chat):
        return chat.get_history()

    def embed(self, content: str):
        """Embed messages with llm"""
        result = self.client.models.embed_content(
            model=self.embedding_model,
            contents=content
        )
        return result.embeddings


class OpenAIClient(LLMClient):
    pass