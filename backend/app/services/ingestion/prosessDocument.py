import os
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.processors.factory import get_processor
from app.services.ingestion.chunker import chunk_page


logger = logging.getLogger(__name__)

BATCH_FLUSH_SIZE = 200  # flush to DB every N chunks

def process_document(document_id: int) -> None:
    
    db = SessionLocal()

    try:

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            raise ValueError(f"Document {document_id} not found")

        logger.info("Started processing document %s (%s)", document.id, document.original_filename)

        # ── Idempotency: wipe any existing chunks first ──────────────
        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).delete(synchronize_session=False)

        document.processing_status = "processing"
        document.processing_started_at = datetime.now(timezone.utc)
        document.processing_error = None    # clear any previous error
        db.flush()  # write status without committing yet

        # ── File guard ────────────────────────────────────────────────
        if not os.path.exists(document.storage_path):
            raise FileNotFoundError(
                f"Storage file missing: {document.storage_path}"
            )

        processor = get_processor(document.mime_type)

        chunk_counter = 0
        batch: list[dict] = []

        for page_content in processor.extract_pages(document.storage_path):
            for chunk in chunk_page(page_content.text, page_content.page_number):
                batch.append({
                    "document_id": document.id,
                    "chunk_index": chunk_counter,
                    "page_number": chunk.page_number,      # ← stored now
                    "content": chunk.text,
                })
                chunk_counter += 1

            # ── Batch flush to avoid holding everything in memory ────
            if len(batch) >= BATCH_FLUSH_SIZE:
                db.bulk_insert_mappings(DocumentChunk, batch)
                batch.clear()

        # ── Final flush for remaining chunks ────────────────────────
        if batch:
            db.bulk_insert_mappings(DocumentChunk, batch)

        document.processing_status = "completed"
        document.chunk_count = chunk_counter
        document.processing_completed_at = datetime.now(timezone.utc)
        db.commit()   # ← single atomic commit
        logger.info("Processing completed: %s chunks", chunk_counter)

    except Exception as e:
        db.rollback()
        logger.error("Failed processing document %s: %s", document_id, e, exc_info=True)

        # re-fetch after rollback since the session state was cleared
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            document.processing_status = "failed"
            document.processing_error = str(e)
            document.processing_completed_at = datetime.now(timezone.utc)
            db.commit()
        raise

    finally:
        db.close()