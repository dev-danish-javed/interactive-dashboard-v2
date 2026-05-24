from llm.llm_clients.factory.LLMClientFactory import LLMClientFactory
from services.prompts import sql_prompt, process_result_query, sql_prompt_2, chart_function_call_prompt
from utils.db_utils.oracle_utils import execute_query
from utils.embedding_utils import EmbeddingUtils
from utils.logger import get_logger


class ChatService:
    _instance = None

    chats : dict = {}
    _next_chat_id: int = 1

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = get_logger("chat_service")

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
            chart_image_tag = None
            self.logger.info(f"Processing message: {message}")
            current_chat = self.chats.get(chat_id)
            self.logger.info(f"Found current chat for chat_id: {chat_id}")
            llm_client = LLMClientFactory.getChatClient()
            self.logger.info(f"Got LLM client as {llm_client.__class__.__name__}")
            embedding_utils = EmbeddingUtils()

            # If server restarted or chat_id invalid, (re)initialize chat for this id
            if current_chat is None:
                current_chat = llm_client.create_chat(sql_prompt_2)
                self.chats[chat_id] = current_chat
            # Build concise relevant context from vector DB (documents only)
            relevant_schema = embedding_utils.query_embeddings(message)
            self.logger.info(f"Got {'empty' if not relevant_schema else 'non-empty'} relevant schema for user query")
            try:
                docs = relevant_schema.get("documents", [])
                if isinstance(docs, list) and len(docs) > 0 and isinstance(docs[0], list):
                    docs = docs[0]
                relevant_context = "\n\n".join(docs) if docs else ""
            except Exception:
                relevant_context = ""

            model_input = f"""User query : {message}
                        
                        Relevant schema : {relevant_context}
                        """
            sql_result= llm_client.get_query_data(current_chat, model_input)
            process_result_prompt = process_result_query
            process_result_prompt = process_result_prompt.replace("<user_query>", model_input).replace("<db_result>", str(sql_result))

            processed_result = llm_client.process_db_result(current_chat, process_result_prompt)

            # Safe guard if LLM didn't return a structured response
            if not processed_result:
                return {'text_response': 'I could not summarize the result. Please try rephrasing your question.', "chart_image_tag": None}

            if getattr(processed_result, 'can_create_chart_on_data', False):
                relevant_schema = embedding_utils.query_embeddings(processed_result.relevant_question_for_chart_data)
                try:
                    docs = relevant_schema.get("documents", [])
                    if isinstance(docs, list) and len(docs) > 0 and isinstance(docs[0], list):
                        docs = docs[0]
                    relevant_context_chart = "\n\n".join(docs) if docs else ""
                except Exception:
                    relevant_context_chart = ""

                # followup_input = f"""User query : {processed_result.relevant_question_for_chart_data}
            if processed_result.can_create_chart_on_data:
                self.logger.info(f"Chart generation possible for the user query")
                relevant_schema = embedding_utils.query_embeddings(processed_result.relevant_question_for_chart_data)
                self.logger.info(f"Got {'empty' if not relevant_schema else 'non-empty'} relevant schema for chart generation relevant question")
                followup_input = f"""User query : {processed_result.relevant_question_for_chart_data}
                        
                        Relevant schema : {relevant_context_chart}
                        """
                sql_result= llm_client.get_query_data(current_chat, followup_input)
                charts_prompt = chart_function_call_prompt.replace('<user_query>', followup_input).replace('<db result>', processed_result.response)
                charts_prompt = charts_prompt.replace('<model_question>', processed_result.relevant_question_for_chart_data)
                charts_prompt = charts_prompt.replace('<model_query_result>', str(sql_result))
                chart_image_tag = llm_client.create_chart(charts_prompt)
                self.logger.info(f"Created chart image tag for the user query")
            
            return {'text_response':processed_result.response, "chart_image_tag" : chart_image_tag}
        except Exception as error:
            self.logger.error(f"Error processing message: {error}")
            return {"text_response": "Sorry, I ran into an issue processing your request.", "chart_image_tag": None}

