from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ок"

def test_register_and_login():
    import uuid
    username = f"user_{uuid.uuid4().hex[:8]}"
    r = client.post("/auth/register", json={"username": username, "password": "secret"})
    assert r.status_code == 200, r.text
    r = client.post("/auth/login", data={"username": username, "password": "secret"})
    assert r.status_code == 200, r.text
    assert "access_token" in r.json()