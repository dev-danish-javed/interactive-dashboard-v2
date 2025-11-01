from llm.llm_clients.factory.LLMClientFactory import LLMClientFactory
from services.prompts import sql_prompt, process_result_query, sql_prompt_2, chart_function_call_prompt
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
        chat = llm_client.create_chat(sql_prompt_2)
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
            sql_result= llm_client.get_query_data(current_chat, message)
            process_result_prompt = process_result_query
            process_result_prompt = process_result_prompt.replace("<user_query>", message).replace("<db_result>", str(sql_result))

            processed_result = llm_client.process_db_result(current_chat, process_result_prompt)
            if processed_result.can_create_chart_on_data:
                relevant_schema = embedding_utils.query_embeddings(processed_result.relevant_question_for_chart_data)
                message = f"""User query : {processed_result.relevant_question_for_chart_data}
                        
                        Relevant schema : {relevant_schema}
                        """
                sql_result= llm_client.get_query_data(current_chat, message)
                charts_prompt = chart_function_call_prompt.replace('<user_query>', message).replace('<db result>', processed_result.response)
                charts_prompt = charts_prompt.replace('<model_question>', processed_result.relevant_question_for_chart_data)
                charts_prompt = charts_prompt.replace('<model_query_result>', sql_result)
                llm_client.create_chat(charts_prompt)
            
            return processed_result
        except Exception as error:
            print(error)




