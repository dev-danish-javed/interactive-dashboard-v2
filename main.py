from fastapi import FastAPI

from routers.chat_router_v2 import chat_router_v2
from routers.embedding_router import embeddings_router, refresh_db_embeddings
from routers.chat_router import chat_router

app = FastAPI()

refresh_db_embeddings()

app.include_router(embeddings_router)

app.include_router(chat_router)
app.include_router(chat_router_v2)
