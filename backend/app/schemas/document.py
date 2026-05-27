from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):

    filename: str
    file_type: str


class DocumentResponse(BaseModel):

    id: int
    notebook_id: int
    filename: str
    original_filename: str
    file_extension: str
    mime_type: str
    file_size: int
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True