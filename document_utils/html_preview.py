import html

from document_utils.sanitize import (
    sanitize_text
)


def format_html_preview(
    text: str
) -> str:

    clean = sanitize_text(
        text
    )

    blocks = []

    for paragraph in clean.split("\n\n"):

        lines = paragraph.splitlines()

        if not lines:
            continue

        escaped_lines = [
            html.escape(line)
            for line in lines
        ]

        first = escaped_lines[0].strip()

        if (
            len(lines) == 1
            and len(first) <= 100
            and (
                first.isupper()
                or first.endswith(":")
            )
        ):

            blocks.append(
                f"<h3>{first}</h3>"
            )

        elif all(
            line.lstrip().startswith(
                ("-", "*")
            )
            for line in lines
        ):

            items = "".join(
                f"<li>{html.escape(line.lstrip()[1:].strip())}</li>"
                for line in lines
            )

            blocks.append(
                f"<ul>{items}</ul>"
            )

        else:

            blocks.append(
                f"<p>{'<br>'.join(escaped_lines)}</p>"
            )

    body = "\n".join(
        blocks
    )

    return f"""
<div class="legal-preview">
{body}
</div>
""".strip()