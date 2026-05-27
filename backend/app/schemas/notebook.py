from datetime import datetime

from pydantic import BaseModel


class NotebookCreate(BaseModel):

    title: str
    description: str | None = None


class NotebookResponse(BaseModel):

    id: int
    title: str
    description: str | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True