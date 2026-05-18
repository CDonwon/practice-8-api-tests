import os
import pytest
from dotenv import load_dotenv
from api_client import ApiClient

load_dotenv()

def safe_json(response):
    try:
        return response.json()
    except ValueError:
        pytest.fail(f"Ответ не является JSON: {response.text}")

def test_user_can_login():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={
            "username": os.getenv("USER_LOGIN"),
            "password": os.getenv("USER_PASSWORD")
        }
    )
    assert response.status_code == 200
    body = safe_json(response)
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_user_cannot_login_with_wrong_password():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={
            "username": os.getenv("USER_LOGIN"),
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401
    body = safe_json(response)
    assert "detail" in body
    assert "Incorrect username or password" in body["detail"]

def test_login_without_username():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={"password": os.getenv("USER_PASSWORD")}
    )
    assert response.status_code == 422
    body = safe_json(response)
    assert "detail" in body

def test_login_without_password():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={"username": os.getenv("USER_LOGIN")}
    )
    assert response.status_code == 422
    body = safe_json(response)
    assert "detail" in body

def test_login_with_empty_username():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={"username": "", "password": os.getenv("USER_PASSWORD")}
    )
    assert response.status_code == 401
    body = safe_json(response)
    assert "detail" in body

def test_login_with_unknown_user():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={"username": "user_1654654632452", "password": "123123"}
    )
    assert response.status_code == 401
    body = safe_json(response)
    assert "detail" in body