from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongo.models.review_document import ReviewDocument
from app.db.mongo.models.moderation_request_document import (
    ModerationRequestDocument,
)
from app.core.config import settings


async def init_mongo(
    url: str = settings.DB_URL, db_name: str = settings.DB_NAME
):
    client = AsyncIOMotorClient(url)
    db = client[db_name]
    await init_beanie(
        database=db,
        document_models=[ReviewDocument, ModerationRequestDocument],
    )
