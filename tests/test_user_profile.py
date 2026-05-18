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

def test_user_can_get_own_profile(user_token):
    client = ApiClient(token=user_token)
    response = client.get("/api/profiles/me")
    assert response.status_code == 200
    body = safe_json(response)
    assert body["message"] == "User profile"
    assert "profile" in body
    assert body["profile"]["username"] == os.getenv("USER_LOGIN")
    assert body["profile"]["role"]["name"] == "user"
    assert body["profile"]["is_active"] is True

def test_user_cannot_get_profile_without_token():
    client = ApiClient()
    response = client.get("/api/profiles/me")
    assert response.status_code == 403
    body = safe_json(response)
    assert "detail" in body

def test_user_cannot_get_profile_with_invalid_token():
    client = ApiClient(token="invalid_token")
    response = client.get("/api/profiles/me")
    assert response.status_code == 401
    body = safe_json(response)
    assert "detail" in body

def test_user_profile_response_has_required_fields(user_token):
    client = ApiClient(token=user_token)
    response = client.get("/api/profiles/me")
    assert response.status_code == 200
    profile = safe_json(response)["profile"]
    for field in ["id", "username", "email", "role", "is_active"]:
        assert field in profile

def test_user_can_get_profile_by_own_account_id(user_token):
    client = ApiClient(token=user_token)
    me_response = client.get("/api/profiles/me")
    assert me_response.status_code == 200
    account_id = safe_json(me_response)["profile"]["id"]

    profile_response = client.get(f"/api/profiles/{account_id}")
    assert profile_response.status_code == 200
    body = safe_json(profile_response)
    assert "profile" in body
    assert body["profile"]["id"] == account_id
    assert body["profile"]["username"] == os.getenv("USER_LOGIN")