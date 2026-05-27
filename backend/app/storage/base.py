from abc import (
    ABC,
    abstractmethod
)


class StorageService(ABC):

    @abstractmethod
    async def upload_file(
        self,
        file_content: bytes,
        storage_path: str,
        content_type: str
    ) -> str:
        pass