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

@pytest.fixture
def user_token():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={
            "username": os.getenv("USER_LOGIN"),
            "password": os.getenv("USER_PASSWORD")
        }
    )
    assert response.status_code == 200, f"Не удалось залогинить пользователя: {response.text}"
    return safe_json(response)["access_token"]

@pytest.fixture
def admin_token():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={
            "username": os.getenv("ADMIN_LOGIN"),
            "password": os.getenv("ADMIN_PASSWORD")
        }
    )
    assert response.status_code == 200, f"Не удалось залогинить админа: {response.text}"
    return safe_json(response)["access_token"]

@pytest.fixture
def moderator_token():
    client = ApiClient()
    response = client.post(
        "/api/auth/login",
        json={
            "username": os.getenv("MODERATOR_LOGIN"),
            "password": os.getenv("MODERATOR_PASSWORD")
        }
    )
    assert response.status_code == 200, f"Не удалось залогинить модератора: {response.text}"
    return safe_json(response)["access_token"]