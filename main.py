from fastapi import FastAPI

from routers.embedding_router import embeddings_router
from routers.chat_router import chat_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(embeddings_router)