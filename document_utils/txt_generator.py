from document_utils.sanitize import (
    sanitize_text
)


def format_txt(text: str) -> bytes:

    clean_text = sanitize_text(
        text
    )

    return clean_text.encode(
        "utf-8"
    )