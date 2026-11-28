from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_lifecycle_demo_page_returns_200_and_contains_lifecycle():
    response = client.get("/lifecycle")

    assert response.status_code == 200
    assert "Lifecycle" in response.text
