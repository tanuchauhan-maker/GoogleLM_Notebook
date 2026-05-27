import aiofiles

from pathlib import Path

from app.storage.base import (
    StorageService
)

from app.core.config import BASE_DIR, settings

STORAGE_ROOT = BASE_DIR / settings.STORAGE_ROOT


class LocalStorageService(
    StorageService
):

    async def upload_file(
        self,
        file_content: bytes,
        storage_path: str,
        content_type: str
    ) -> str:

        full_path = (
            STORAGE_ROOT / storage_path
        )

        # code creates directories automatically
        full_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        async with aiofiles.open(
            full_path,
            "wb"
        ) as f:

            await f.write(file_content)

        return str(full_path)
