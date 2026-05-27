import boto3

from app.core.config import settings

from app.storage.base import (
    StorageService
)


class S3StorageService(
    StorageService
):

    def __init__(self):

        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

    def upload_file(
        self,
        file_content: bytes,
        storage_path: str,
        content_type: str
    ) -> str:

        self.client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=storage_path,
            Body=file_content,
            ContentType=content_type
        )

        return storage_path