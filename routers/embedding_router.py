from fastapi import APIRouter
from starlette.responses import JSONResponse

from utils.db_utils.oracle_utils import get_db_schema, schema_to_text
from utils.embedding_utils import EmbeddingUtils

embeddings_router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)

@embeddings_router.get("/db")
async def refresh_db_embeddings():
    embedding_utils = EmbeddingUtils()
    try:
        schmea = get_db_schema()
        schema_text = schema_to_text(schmea)
        db_embeddings, chunk_texts = embedding_utils.create_embedding(schema_text)
        embedding_utils.store_embeddings(db_embeddings, chunk_texts)
        return JSONResponse(status_code=200, content={"status":"SUCCESS"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "FAILED", "error": str(e)})


