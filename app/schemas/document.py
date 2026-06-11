from pydantic import BaseModel, Field
from typing import Optional


class DocumentCreate(BaseModel):

    user_id: str = Field(..., min_length=1)

    title: str = Field(..., min_length=1)

    content: str = Field(..., min_length=10)


class DocumentResponse(BaseModel):

    document_id: str

    status: str


class DocumentStatusResponse(BaseModel):

    document_id: str

    status: str

    summary: Optional[str] = None

    error: Optional[str] = None

from typing import List

class UserDocumentItem(BaseModel):

    document_id: str

    title: str

    status: str


class UserDocumentListResponse(
    BaseModel
):

    total: int

    page: int

    page_size: int

    data: List[
        UserDocumentItem
    ]