import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiDocumentGenerator:

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):

        self.api_key = (
            api_key
            or os.getenv(
                "GEMINI_API_KEY",
                ""
            ).strip()
        )

        self.model_name = (
            model_name
            or os.getenv(
                "GEMINI_MODEL",
                "gemini-3.8-flash"
            ).strip()
        )

        self._client = None

    def _get_client(self):

        if self._client is not None:
            return self._client

        if not self.api_key:

            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Add it to the .env file."
            )

        try:

            self._client = genai.Client(
                api_key=self.api_key
            )

        except Exception as exc:

            raise RuntimeError(
                "Could not initialize Gemini client."
            ) from exc

        return self._client

    @staticmethod
    def build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        term_list = [
            item.strip()
            for item in terms.split(";")
            if item.strip()
        ]

        formatted_terms = "\n".join(
            f"- {item}"
            for item in term_list
        )

        if not formatted_terms:

            formatted_terms = (
                f"- {terms.strip()}"
            )

        prompt = f"""
You are LegalEase, an AI-assisted
legal document drafting system.

Draft a professional legal-document TEMPLATE
based only on the supplied facts.

Do not invent names, dates, addresses,
payment amounts, governing law, statutes,
registration details, or other material facts.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{dates}

KEY TERMS:
{formatted_terms}

Requirements:

1. Use clear formal legal language.

2. Include a title and sensible sections
appropriate for the document type.

3. Preserve all supplied facts accurately.

4. Convert the supplied key terms into
coherent clauses.

5. Add clearly marked placeholders such as
[GOVERNING LAW] only where a standard
document normally needs information that
was not supplied.

6. Do not claim the document is legally valid,
legally reviewed, or jurisdiction-specific.

7. End with signature blocks appropriate
to the parties.

8. Return plain text only.

9. Do not use Markdown code fences.

10. Make the document professional,
structured and readable.

This is an AI-assisted draft and must be
reviewed before legal use.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        client = self._get_client()

        prompt = self.build_prompt(
            document_type,
            parties,
            terms,
            dates
        )

        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=6000
            )
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()