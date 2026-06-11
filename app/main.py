from fastapi import FastAPI

import asyncio

from app.db.mongodb import db
from app.db.redis import redis_client

from app.api.documents import (
    router as document_router
)

from app.worker.worker import (
    worker_loop
)

app = FastAPI(
    title="Document Insights API"
)


# @app.on_event("startup")
# async def startup_event():
#
#     asyncio.create_task(
#         worker_loop()
#     )
#


import os
#
# print(
#     "PYTEST_RUNNING =",
#     os.getenv("PYTEST_RUNNING")
# )

@app.on_event("startup")
async def startup_event():

    if os.getenv("PYTEST_RUNNING") != "1":

        asyncio.create_task(
            worker_loop()
        )


@app.get("/")
async def home():

    return {
        "message": "running"
    }


@app.get("/health")
async def health():

    try:
        await db.command("ping")
        mongo_status = "healthy"

    except Exception:
        mongo_status = "unhealthy"

    try:
        redis_client.ping()
        redis_status = "healthy"

    except Exception:
        redis_status = "unhealthy"

    return {
        "mongodb": mongo_status,
        "redis": redis_status
    }


app.include_router(
    document_router
)