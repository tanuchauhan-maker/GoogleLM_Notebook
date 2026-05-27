from app.utils.document import generate_unique_filename, calculate_file_hash

from uuid import uuid4

# from app.storage.s3 import (
#     S3StorageService
# )

from app.storage.local_storage import LocalStorageService

# storage_service = S3StorageService()
storage_service = LocalStorageService()


async def upload_document_file(
    user_id: int,
    notebook_id: int,
    original_filename: str,
    file_content: bytes,
    content_type: str
):
    
    unique_filename = generate_unique_filename(
        original_filename
    )

    storage_path = (
        f"users/{user_id}/"
        f"notebooks/{notebook_id}/"
        f"documents/{unique_filename}"
    )

    uploaded_path = await storage_service.upload_file(
        file_content=file_content,
        storage_path=storage_path,
        content_type=content_type
    )

    file_hash = calculate_file_hash(
        file_content
    )

    return {
        "filename": unique_filename,
        "storage_path": uploaded_path,
        "content_hash": file_hash
    }