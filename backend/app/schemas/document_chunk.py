from datetime import datetime

from pydantic import BaseModel


class ChunkResponse(BaseModel):

    id: int
    document_id: int
    chunk_index: int
    content: str
    metadata_json: dict | None
    created_at: datetime

    class Config:
        from_attributes = True