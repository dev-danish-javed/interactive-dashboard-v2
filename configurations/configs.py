import os
from dotenv import load_dotenv

load_dotenv()

def get_embeddings_client_api_key() -> str:
    return os.getenv("GEMINI_API_KEY")

def get_vector_db_collection_name() -> str:
    return os.getenv("VECTOR_DB_COLLECTION")

def get_embedding_model() -> str:
    return os.getenv("EMBEDDING_MODEL")

def get_db_uri() -> str:
    return os.getenv("DB_URI")

def get_chat_client_api_key()->str:
    return os.getenv("CHAT_API_KEY")

def get_chat_base_url() -> str:
    return os.getenv("CHAT_BASE_URL")

def get_chat_llm_model() -> str:
    return os.getenv("CHAT_LLM_MODEL")