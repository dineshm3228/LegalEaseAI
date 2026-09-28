from fastapi.testclient import (
    TestClient
)

import backend.routes as routes

from backend.main import app


class FakeGenerator:

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        return (
            f"{document_type}\n\n"
            f"Parties: {parties}\n"
            f"Date: {dates}\n"
            f"Terms: {terms}"
        )


def test_health():

    client = TestClient(
        app
    )

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_generate_endpoint():

    original = routes._generator

    routes._generator = (
        FakeGenerator()
    )

    try:

        client = TestClient(
            app
        )

        response = client.post(
            "/generate",
            json={
                "document_type": "NDA",
                "parties": "Alice, Bob",
                "terms": (
                    "Confidentiality;"
                    "Return information"
                ),
                "dates": "April 15, 2025"
            }
        )

        assert (
            response.status_code
            == 200
        )

        body = response.json()

        assert (
            body["document_type"]
            == "NDA"
        )

        assert (
            "Confidentiality"
            in body["content"]
        )

    finally:

        routes._generator = (
            original
        )