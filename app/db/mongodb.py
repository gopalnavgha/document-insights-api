# from motor.motor_asyncio import AsyncIOMotorClient
#
# from app.core.config import settings
#
# client=AsyncIOMotorClient(
#     settings.MONGO_URI
# )
#
# db=client[
#     settings.DB_NAME
# ]

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(
    settings.MONGO_URI
)

db = client[settings.DB_NAME]

documents_collection = db.documents