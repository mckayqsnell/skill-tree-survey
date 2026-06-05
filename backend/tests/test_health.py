"""Smoke tests: the app boots (lifespan + seeding run) and core endpoints respond."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "healthy"
    assert body["name"]


def test_create_session_round_trip():
    """A survey session can be created and read back (exercises DB + DAO/Service/Route)."""
    with TestClient(app) as client:
        created = client.post(
            "/api/sessions/",
            json={"user_name": "Test User", "user_email": "test@example.com"},
        )
        assert created.status_code in (200, 201), created.text
        session_id = created.json()["id"]

        fetched = client.get(f"/api/sessions/{session_id}")
    assert fetched.status_code == 200
    assert fetched.json()["user_email"] == "test@example.com"
