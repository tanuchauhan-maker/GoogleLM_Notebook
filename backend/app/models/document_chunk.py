from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    JSON,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

#Why Keep Chunks in PostgreSQL?
#Because vector DBs are NOT your source of truth. Main Db should maintain the ownership, refrences etc


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )

    chunk_index = Column(Integer, nullable=False)

    page_number = Column(Integer, nullable=True)

    content = Column(Text, nullable=False)

    metadata_json = Column(JSON)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )