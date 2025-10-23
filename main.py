from fastapi import FastAPI

from routers.embedding_router import embeddings_router, refresh_db_embeddings
from routers.chat_router import chat_router

app = FastAPI()

refresh_db_embeddings()

app.include_router(chat_router)
app.include_router(embeddings_router)