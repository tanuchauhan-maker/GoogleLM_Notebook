from langchain_text_splitters import RecursiveCharacterTextSplitter
from dataclasses import dataclass

# Instantiate ONCE — not per page
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

@dataclass
class Chunk:
    text: str
    page_number: int
    chunk_index_on_page: int

def chunk_page(text: str, page_number: int) -> list[Chunk]:
    pieces = _splitter.split_text(text)
    return [
        Chunk(text=piece, page_number=page_number, chunk_index_on_page=i)
        for i, piece in enumerate(pieces)
    ]