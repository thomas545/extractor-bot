from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_headers():
    return {"Content-Type": "application/json"}


def test_success_signup_api():
    body = {"username": "test", "email": "test@gmail.com", "password": "123456thomas"}
    response = client.post("/auth/signup/", json=body, headers=get_headers())
    assert response.status_code == 200


def test_failed_signup_api():
    body = {"username": "test", "email": "test@gmail.com", "password": "123456thomas"}
    response = client.post("/auth/signup/", json=body, headers=get_headers())
    assert response.status_code == 400


def test_login_api():
    body = {"email": "test@gmail.com", "password": "123456thomas"}
    response = client.post("/auth/login/", json=body, headers=get_headers())
    assert response.status_code == 200
    assert "access_token" in response.json().get("data")
