from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers.chat_router import chat_router
from routers.embedding_router import embeddings_router, refresh_db_embeddings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await refresh_db_embeddings()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(embeddings_router)
app.include_router(chat_router)
