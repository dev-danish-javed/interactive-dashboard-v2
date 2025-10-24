from configurations.configs import get_chat_llm_client
from llm_clients.LLMClient import LLMClient, LLMClients, GeminiClient, OpenAIClient
from routers.chat_router import ChatModel

class LLMClientFactory:
    @staticmethod
    def getChatClient() -> LLMClient:
        chat_llm : LLMClients = LLMClients(get_chat_llm_client())
        if chat_llm is LLMClients.GEMINI:
            return GeminiClient()
        elif chat_llm is LLMClients.OPENAI:
            return OpenAIClient()
        else:
            raise Exception("Unknown llm client")