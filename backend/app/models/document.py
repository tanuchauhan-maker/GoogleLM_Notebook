from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    BigInteger,
    Text
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.core.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    notebook_id = Column(
        Integer,
        ForeignKey("notebooks.id"),
        nullable=False
    )

    filename = Column(
        String,
        nullable=False
    )

    original_filename = Column(
        String,
        nullable=False
    )

    file_extension = Column(
        String,
        nullable=False
    )

    mime_type = Column(
        String,
        nullable=False
    )

    file_size = Column(
        BigInteger,
        nullable=False
    )

    storage_path = Column(
        Text,
        nullable=False
    )

    content_hash = Column(
        String,
        nullable=False
    )

    processing_status = Column(
        String,
        default="pending"
    )

    processing_started_at   = Column(
        DateTime(timezone=True), 
        nullable=True
    )

    processing_completed_at = Column(
        DateTime(timezone=True), 
        nullable=True
    )

    processing_error = Column(
        Text, 
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    notebook = relationship(
        "Notebook",
        back_populates="documents"
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete"
    )