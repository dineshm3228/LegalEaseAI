from fpdf import FPDF

from document_utils.sanitize import (
    sanitize_text
)


class LegalEasePDF(FPDF):

    def __init__(
        self,
        doc_type: str
    ):

        super().__init__()

        self.doc_type = sanitize_text(
            doc_type
        )

        self.set_auto_page_break(
            auto=True,
            margin=18
        )

    def header(self):

        self.set_font(
            "Times",
            "B",
            16
        )

        self.cell(
            0,
            8,
            "LEGALEASE",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        self.set_font(
            "Times",
            "B",
            12
        )

        self.cell(
            0,
            7,
            self.doc_type,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        self.ln(3)

    def footer(self):

        self.set_y(-14)

        self.set_font(
            "Times",
            "",
            8
        )

        self.cell(
            0,
            6,
            "LegalEase - AI-assisted draft. "
            "Review before legal use.",
            align="C"
        )


def format_pdf(
    text: str,
    doc_type: str
) -> bytes:

    pdf = LegalEasePDF(
        doc_type
    )

    pdf.set_title(
        f"LegalEase - {doc_type}"
    )

    pdf.add_page()

    pdf.set_font(
        "Times",
        "",
        11
    )

    clean = sanitize_text(
        text
    )

    for block in clean.split(
        "\n\n"
    ):

        block = block.strip()

        if not block:
            continue

        lines = block.splitlines()

        # Heading
        if (
            len(lines) == 1
            and len(lines[0]) <= 100
            and (
                lines[0].isupper()
                or lines[0].endswith(":")
            )
        ):

            pdf.set_font(
                "Times",
                "B",
                12
            )

            pdf.multi_cell(
                0,
                7,
                lines[0],
                new_x="LMARGIN",
                new_y="NEXT"
            )

            pdf.ln(2)

            pdf.set_font(
                "Times",
                "",
                11
            )

            continue

        for line in lines:

            stripped = line.strip()

            if stripped.startswith(
                ("-", "*")
            ):

                pdf.multi_cell(
                    0,
                    6,
                    "- "
                    + stripped[1:].strip(),
                    new_x="LMARGIN",
                    new_y="NEXT"
                )

            else:

                pdf.multi_cell(
                    0,
                    6,
                    stripped,
                    new_x="LMARGIN",
                    new_y="NEXT"
                )

        pdf.ln(3)

    output = pdf.output(
        dest="S"
    )

    if isinstance(
        output,
        str
    ):

        return output.encode(
            "latin-1"
        )

    return bytes(
        output
    )