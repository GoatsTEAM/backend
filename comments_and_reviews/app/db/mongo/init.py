from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongo.models.review_document import ReviewDocument
from app.db.mongo.models.moderation_request_document import (
    ModerationRequestDocument,
)


async def init_mongo(url: str, db_name: str):
    client = AsyncIOMotorClient(url)
    db = client[db_name]
    await init_beanie(
        database=db,
        document_models=[ReviewDocument, ModerationRequestDocument],
    )
