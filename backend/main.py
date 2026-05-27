from fastapi import FastAPI

from app.core.database import (
    Base,
    engine
)

from app.api.routes import (
    notebooks,
    documents,
    auth,
    chat_sessions,
    messages
)

from app.models.user import User
from app.models.notebook import Notebook
from app.models.document import Document
from app.models.chat_session import ChatSession
from app.models.message import Message
from app.models.document_chunk import DocumentChunk


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(notebooks.router)
app.include_router(documents.router)
app.include_router(chat_sessions.router)
app.include_router(messages.router)

Base.metadata.create_all(
    bind=engine
)
