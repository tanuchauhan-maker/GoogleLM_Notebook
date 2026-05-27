from app.processors.pdf_processor import PDFProcessor

from app.processors.text_processor import TextProcessor

# To select the proocessor for diffrent types of files
def get_processor(
    mime_type: str
):

    if mime_type == "application/pdf":

        return PDFProcessor()

    elif mime_type.startswith("text"):

        return TextProcessor()

    raise ValueError(
        f"Unsupported file type: {mime_type}"
    )

