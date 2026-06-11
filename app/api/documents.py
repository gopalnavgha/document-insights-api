from fastapi import APIRouter

from app.schemas.document import (
    DocumentCreate,
    DocumentResponse
)

router = APIRouter()


from app.db.mongodb import documents_collection
from datetime import datetime
import hashlib


@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201
)
async def create_document(
        payload: DocumentCreate
):
    #Before content_hash generation i added this ############################
    if not RateLimitService.can_submit_job(
            payload.user_id
    ):
        raise HTTPException(
            status_code=429,
            detail=(
                "Maximum active jobs "
                "limit reached"
            )
        )


    ########################################
    content_hash = hashlib.sha256(
        payload.content.encode()
    ).hexdigest()
######################################################
    cached_summary = (
        CacheService.get_summary(
            payload.user_id,
            content_hash
        )
    )

    if cached_summary:
        return {
            "document_id": "cached",
            "status": "completed"
        }
#################################################
    document = {
        "user_id": payload.user_id,
        "title": payload.title,
        "content": payload.content,

        "content_hash": content_hash,

        "status": "queued",

        "summary": None,

        "error": None,

        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }


    result = await documents_collection.insert_one(
        document
    )

    RateLimitService.increment_job(
        payload.user_id
    )

    return {
        "document_id": str(result.inserted_id),
        "status": "queued"
    }


from bson import ObjectId

from fastapi import HTTPException

from app.schemas.document import (
    DocumentStatusResponse
)


from app.utils.objectid import (
    is_valid_objectid
)



@router.get(
    "/documents/{document_id}",
    response_model=DocumentStatusResponse
)
async def get_document(
    document_id: str
):

    if not is_valid_objectid(
        document_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    document = await documents_collection.find_one(
        {
            "_id": ObjectId(
                document_id
            )
        }
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "document_id": str(
            document["_id"]
        ),

        "status": document["status"],

        "summary": document.get(
            "summary"
        ),

        "error": document.get(
            "error"
        )
    }


from fastapi import Query

from app.schemas.document import (
    UserDocumentListResponse,
    UserDocumentItem
)

@router.get(
    "/users/{user_id}/documents",
    response_model=UserDocumentListResponse
)
async def get_user_documents(
    user_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: str | None = None
):

    query = {
        "user_id": user_id
    }

    if status:
        query["status"] = status

    total = await documents_collection.count_documents(
        query
    )

    skip = (
        page - 1
    ) * page_size

    cursor = (
        documents_collection
        .find(query)
        .skip(skip)
        .limit(page_size)
        .sort("created_at", -1)
    )

    documents = []

    async for doc in cursor:

        documents.append(
            UserDocumentItem(
                document_id=str(
                    doc["_id"]
                ),
                title=doc["title"],
                status=doc["status"]
            )
        )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": documents
    }



from app.services.rate_limit_service import (
    RateLimitService
)

from fastapi import HTTPException

from app.services.cache_service import CacheService