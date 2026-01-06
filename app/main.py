import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.database import Base, engine

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# In a real microservice, you'd use Alembic for migrations.
# For this implementation, we'll create tables on startup if they don't exist.
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # This will create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
