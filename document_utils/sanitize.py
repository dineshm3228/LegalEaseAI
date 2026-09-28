import re
import unicodedata


def sanitize_text(text: str) -> str:

    if not isinstance(text, str):
        return ""

    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2212": "-",

        "\u00a0": " ",

        "\u2022": "-",

        "\u200b": "",
        "\ufeff": ""
    }

    for source, target in replacements.items():

        text = text.replace(
            source,
            target
        )

    text = unicodedata.normalize(
        "NFKC",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()