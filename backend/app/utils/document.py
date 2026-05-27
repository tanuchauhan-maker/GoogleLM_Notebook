import hashlib

from pathlib import Path

from uuid import uuid4


STORAGE_ROOT = Path("storage")


def generate_unique_filename(
    extension: str
) -> str:

    return f"{uuid4()}{extension}"


def calculate_file_hash(
    content: bytes
) -> str:

    return hashlib.sha256(content).hexdigest()