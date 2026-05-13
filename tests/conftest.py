import os

import pytest
from dotenv import load_dotenv

from api_client import ApiClient


load_dotenv()


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

    assert response.status_code == 200
    return response.json()["access_token"]


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

    assert response.status_code == 200
    return response.json()["access_token"]