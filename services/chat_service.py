from llm_clients.factory.LLMClientFactory import LLMClientFactory
from services.prompts import sql_prompt, process_result_query
from utils.db_utils.oracle_utils import execute_query
from utils.embedding_utils import EmbeddingUtils


class ChatService:
    _instance = None

    chats : dict = {}
    _next_chat_id: int = 1

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_chat(self) -> str:
        """Creates a new chat and returns its id"""
        new_chat_id = "ch-"+str(self._next_chat_id)
        llm_client = LLMClientFactory.getChatClient()
        chat = llm_client.create_chat(sql_prompt)
        self.chats[new_chat_id] = chat
        self._next_chat_id += 1
        return new_chat_id

    def get_chat(self, chat_id:str) -> list:
        """Returns entire chat"""
        llm_client = LLMClientFactory.getChatClient()
        return llm_client.get_chat_history(self.chats.get(chat_id))

    def ping(self, chat_id:str, message):
        """Process messages with llm"""
        try:
            current_chat = self.chats.get(chat_id)
            llm_client = LLMClientFactory.getChatClient()
            embedding_utils = EmbeddingUtils()
            relevant_schema = embedding_utils.query_embeddings(message)
            message = f"""User query : {message}
                        
                        Relevant schema : {relevant_schema}
                        """
            sql_command= llm_client.ping(current_chat, message)
            sql_result = execute_query(sql_command)
            process_result_prompt = process_result_query
            process_result_prompt = process_result_prompt.replace("<user_query>", message).replace("<sql_query>", sql_command).replace("<db_result>", str(sql_result))

            return llm_client.ping(current_chat, process_result_prompt)
        except Exception as error:
            print(error)




