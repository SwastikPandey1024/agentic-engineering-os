from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "production-service"
    assert data["version"] == "1.0.0"


def test_request_id_header():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert "X-Request-ID" in response.headers
