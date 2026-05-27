import fitz
import io
import pytesseract
from PIL import Image
from typing import Iterator
from dataclasses import dataclass

@dataclass
class PageContent:
    text: str
    page_number: int       # 1-indexed
    has_images: bool

class PDFProcessor:
    MIN_WORD_COUNT = 20    # skip pages with fewer words than this

    def extract_pages(self, file_path: str) -> Iterator[PageContent]:
        document = fitz.open(file_path)
        try:
            for page in document:
                text = page.get_text()

                # Extract + OCR images on this page
                for img in page.get_images(full=True):
                    try:
                        xref = img[0]
                        base_image = document.extract_image(xref)
                        pil_img = Image.open(io.BytesIO(base_image["image"]))
                        ocr_text = pytesseract.image_to_string(pil_img)
                        if ocr_text.strip():
                            text += f"\n[IMAGE: {ocr_text.strip()}]"
                    except Exception:
                        pass  # don't let a bad image kill the whole doc

                word_count = len(text.split())
                if word_count < self.MIN_WORD_COUNT:
                    continue

                yield PageContent(
                    text=text,
                    page_number=page.number + 1,
                    has_images=len(page.get_images()) > 0
                )
        finally:
            document.close()