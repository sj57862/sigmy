from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_register_success():
    response = client.post(
        "auth/register",
        data={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 200