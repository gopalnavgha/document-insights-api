import asyncio
import random

from datetime import datetime

from app.db.mongodb import documents_collection

from app.services.rate_limit_service import (
    RateLimitService
)

from app.services.cache_service import (
    CacheService
)


def generate_summary(content: str):

    words = content.split()

    return " ".join(words[:20]) + "..."


async def process_document(document):

    document_id = document["_id"]

    user_id = document["user_id"]

    await documents_collection.update_one(
        {
            "_id": document_id
        },
        {
            "$set": {
                "status": "processing",
                "updated_at": datetime.utcnow()
            }
        }
    )

    wait_time = random.randint(10, 30)

    await asyncio.sleep(wait_time)

    fail = random.random() < 0.1

    if fail:

        await documents_collection.update_one(
            {
                "_id": document_id
            },
            {
                "$set": {
                    "status": "failed",
                    "error": "Processing failed",
                    "updated_at": datetime.utcnow()
                }
            }
        )

        RateLimitService.decrement_job(
            user_id
        )

        return

    summary = generate_summary(
        document["content"]
    )

    CacheService.set_summary(
        user_id,
        document["content_hash"],
        summary
    )

    await documents_collection.update_one(
        {
            "_id": document_id
        },
        {
            "$set": {
                "status": "completed",
                "summary": summary,
                "updated_at": datetime.utcnow()
            }
        }
    )

    RateLimitService.decrement_job(
        user_id
    )


async def worker_loop():

    while True:

        document = await documents_collection.find_one(
            {
                "status": "queued"
            }
        )

        if not document:

            await asyncio.sleep(3)

            continue

        try:

            await process_document(
                document
            )

        except Exception as e:

            print(
                f"Worker Error: {str(e)}"
            )

            await asyncio.sleep(2)