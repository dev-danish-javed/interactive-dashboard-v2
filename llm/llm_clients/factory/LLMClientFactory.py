from configurations.configs import get_chat_llm_client
from llm.llm_clients.LLMClient import LLMClient, LLMClients, GeminiClient, OpenAIClient
from utils.logger import get_logger

class LLMClientFactory:
    @staticmethod
    def getChatClient() -> LLMClient:
        logger = get_logger("LLMClientFactory")
        chat_llm : LLMClients = LLMClients(get_chat_llm_client())
        if chat_llm is LLMClients.GEMINI:
            logger.info(f"Creating  GeminiClient")
            return GeminiClient()
        elif chat_llm is LLMClients.OPENAI:
            logger.info(f"Creating  OpenAIClient")
            return OpenAIClient()
        else:
            logger.error(f"Unknown llm client: {chat_llm}")
            raise Exception("Unknown llm client")