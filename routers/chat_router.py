import logging
import uuid
from typing import List

from fastapi import APIRouter
from openai import OpenAI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from configurations.configs import get_chat_client_api_key, get_chat_base_url, get_chat_llm_model
from utils.db_utils.oracle_utils import execute_query
from utils.embedding_utils import EmbeddingUtils


class ChatModel(BaseModel):
    chat_id: str
    messages: List[str]
    new_messages: str


chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

embeddingUtils = EmbeddingUtils()
# embeddingUtils = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=get_chat_client_api_key(),
    base_url=get_chat_base_url()
)


chats={}
application_prompt = {"role": "system", "content": f"""You are an expert Oracle SQL assistant. The database you are working on is oracle db.
                        Use only the provided database schema to answer queries.
                        STRICT OUTPUT RULES:
                        - Output ONLY raw SQL text.
                        - Do not wrap the sql in markdown
                        - Always return a valid Oracle SQL script.
                        - Do not add a trailing semicolon.

                        Example of correct output:
                            SELECT * FROM users

                        Example of wrong output:
                            ```sql
                            SELECT * FROM users;
                            ```
                        """}

# Generate a new chat
@chat_router.get("/start")
async def chat() -> JSONResponse:
    """
    Generate a new chat
    :return:
    """
    # generate a chat id
    unique_id = str(uuid.uuid4())
    # make entry in chat array
    chats[unique_id] = [application_prompt]
    # return tha chat id
    return JSONResponse( status_code=200, content={"chat_id": unique_id})


@chat_router.get("/{chat_id}")
async def chat(chat_id: str) -> JSONResponse:
    """
    Returns the entire chat by id
    :param chat_id:
    :return:
    """
    if chat_id not in chats:
        return JSONResponse(status_code=404, content={"chat_id": chat_id})

    return JSONResponse(status_code=200, content=chats[chat_id])

@chat_router.post("/message")
async def add_chat(request: ChatModel) -> JSONResponse:
    """
    Adds new message to the chat
    :param chat_id:
    :param message:
    :return:
    """
    try:
        chat_id = request.chat_id
        message = request.new_messages
        logger.info(f"Adding new message to chat: {chat_id}")
        if chat_id not in chats  or message is None:
            logger.warning(f"Invalid chat requested: {chat_id}")
            return JSONResponse(status_code=404, content={"chat_id": chat_id})

        chat = chats[chat_id]

        logger.info("User query:", message)
        relevant_schema = embeddingUtils.query_embeddings(message)
        logger.info(f"Relevant schema: {relevant_schema}")
        system_prompt = {"role": "system", "content": f"""
                        For user query:  {message}
                        Below is the relevant schema:
                        {relevant_schema}
                        """}
        user_prompt = {"role": "user", "content": message}

        chat.append(system_prompt)
        chat.append(user_prompt)

        sql_response = client.chat.completions.create(
            model=get_chat_llm_model(),
            messages=chat
        )

        sql_query = sql_response.choices[0].message.content
        logger.info(f"SQL query: {sql_query}")
        query_result = execute_query(sql_query)
        chat.append({"role": "assistant", "content": f"sql: {sql_query}"})
        process_result_query = f"""You are a helpful assistant. 
                                        Your task is to process user query and provide them response.
                                        A user has asked you this question: {message}
                                        DBA executed this sql query : {sql_query}
                                        This is the result from db: {query_result}
                                        Your task is to create a beautiful well structured response for the user"""

        chat.append({"role": "user", "content": f"""{process_result_query}"""})

        result_response = client.chat.completions.create(
            model=get_chat_llm_model(),
            messages=chat
        )

        return JSONResponse(status_code=200, content={"chat_id": result_response.choices[0].message.content})
    except Exception as error:
        return JSONResponse(status_code=500, content={"error": str(error)})