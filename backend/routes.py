import os

from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)


router = APIRouter(
    tags=["documents"]
)


_generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        content = _generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=content
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        detail = (
            "Document generation failed. "
            "Check the backend logs and Gemini configuration."
        )

        if os.getenv(
            "DEBUG",
            ""
        ).lower() == "true":

            detail = str(exc)

        raise HTTPException(
            status_code=502,
            detail=detail
        ) from exc