from datetime import datetime
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_readiness():
    pre_utc_dt = datetime.utcnow()
    response = client.get("/readiness")
    assert response.status_code == 200
    assert datetime.fromisoformat(response.json()["utc_dt"]) >= pre_utc_dt

def test_liveness():
    response = client.get("/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "Success"}

def test_swagger():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text