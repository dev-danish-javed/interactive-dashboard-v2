import logging
from fastapi import APIRouter
from starlette.responses import JSONResponse
from pathlib import Path

from utils.db_utils.oracle_utils import get_db_schema, schema_to_text, get_packages_source_text
from utils.embedding_utils import EmbeddingUtils

embeddings_router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)

@embeddings_router.get("/db")
async def refresh_db_embeddings():
    logger = logging.getLogger(__name__)
    logger.info("GET /embeddings/db - Refreshing database embeddings")
    embedding_utils = EmbeddingUtils()
    try:
        schmea = get_db_schema()
        schema_text = schema_to_text(schmea)

        # Prefer fetching package sources from DB; fallback to repository files if empty
        packages_text = get_packages_source_text()
        if not packages_text:
            packages_dir = Path("Database/packages")
            file_texts = []
            if packages_dir.exists() and packages_dir.is_dir():
                for sql_file in packages_dir.glob("*.sql"):
                    try:
                        file_texts.append(sql_file.read_text(encoding="utf-8"))
                    except Exception:
                        file_texts.append(sql_file.read_text())
            if file_texts:
                packages_text = "\n\n-- Oracle Packages (files) --\n" + "\n\n".join(file_texts)

        full_text = schema_text + ("\n\n-- Oracle Packages (from DB) --\n" + packages_text if packages_text else "")

        db_embeddings, chunk_texts = embedding_utils.create_embedding(full_text)
        embedding_utils.store_embeddings(db_embeddings, chunk_texts)
        logger.info("/embeddings/db - Embeddings refresh SUCCESS")
        return JSONResponse(status_code=200, content={"status":"SUCCESS"})
    except Exception as e:
        logger.exception("/embeddings/db - Embeddings refresh FAILED")
        return JSONResponse(status_code=500, content={"status": "FAILED", "error": str(e)})


