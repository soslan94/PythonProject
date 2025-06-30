from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_users():
    with TestClient(app) as client:
        response = client.get("/users/users/")
        assert response.status_code == 200

