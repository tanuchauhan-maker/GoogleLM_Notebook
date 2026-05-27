from app.processors.base import (
    BaseProcessor
)


class TextProcessor(
    BaseProcessor
):

    def extract_text(
        self,
        file_path: str
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()