from document_utils.sanitize import (
    sanitize_text
)


def test_sanitize_typographic_characters():

    text = (
        "“Hello” — world\u00a0"
    )

    assert sanitize_text(
        text
    ) == '"Hello" - world'


def test_sanitize_blank_lines():

    result = sanitize_text(
        "a\n\n\n\nb"
    )

    assert result == (
        "a\n\nb"
    )