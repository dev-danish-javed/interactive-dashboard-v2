import logging
import uuid
from typing import List

from fastapi import APIRouter
from openai import OpenAI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from configurations.configs import get_chat_client_api_key, get_chat_base_url, get_chat_llm_model
from services.chat_service import ChatService
from utils.db_utils.oracle_utils import execute_query
from utils.embedding_utils import EmbeddingUtils


class ChatModel(BaseModel):
    chat_id: str
    messages: List[str]
    new_message: str


chat_router_v2 = APIRouter(
    prefix="/chat-v2",
    tags=["Chat-v2"]
)

chat_service = ChatService()
embeddingUtils = EmbeddingUtils()
# embeddingUtils = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# Generate a new chat
@chat_router_v2.get("/start")
async def chat() -> JSONResponse:
    """
    Generate a new chat
    :return: chat_id
    """
    # create and return the chat id
    return JSONResponse( status_code=200, content={"chat_id": chat_service.create_chat()})


@chat_router_v2.get("/{chat_id}")
async def chat(chat_id: str) -> JSONResponse:
    """
    Returns the entire chat by id
    :param chat_id:
    :return:
    """
    return JSONResponse(chat_service.get_chat(chat_id))
    pass

@chat_router_v2.post("/message")
async def add_chat(request: ChatModel) -> JSONResponse:
    """
    Adds new message to chat
    :param request:
    :return:
    """
    try:
        return JSONResponse(chat_service.ping(request.chat_id, request.new_message))

    except Exception as error:
        return JSONResponse(status_code=500, content={"error": str(error)})