"""Regression tests: unauthorized API requests must return a real 401 with JSON.

Before the fix, a global 401 handler rendered an HTML page with status 200,
so a failed login looked successful to API clients.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed import seed

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_db():
    seed(reset=True)
    yield


def test_wrong_password_returns_401():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_wrong_password_returns_json_not_html():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )
    assert response.headers["content-type"].startswith("application/json")
    assert "detail" in response.json()


def test_unknown_email_returns_401():
    response = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )
    assert response.status_code == 401


def test_failed_login_does_not_leak_user_or_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )
    body = response.text
    assert "user" not in response.json()
    assert "admin-dev" not in body


def test_successful_login_still_returns_200_without_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "admin-dev"},
    )
    assert response.status_code == 200
    user = response.json()["user"]
    assert user["role"] == "admin"
    assert "password" not in user
    assert "password_hash" not in user


def test_unauthorized_page_outside_api_is_still_html_with_401_status():
    """Browser routes keep the friendly HTML page, but with the right status."""
    from fastapi import HTTPException

    @app.get("/__test_unauthorized__")
    async def _raise_unauthorized():
        raise HTTPException(status_code=401, detail="unauthorized")

    response = client.get("/__test_unauthorized__")
    assert response.status_code == 401
    assert response.headers["content-type"].startswith("text/html")
