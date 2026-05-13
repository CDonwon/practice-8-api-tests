import os

from dotenv import load_dotenv

from api_client import ApiClient


load_dotenv()


def test_user_can_get_own_profile(user_token):
    client = ApiClient(token=user_token)

    response = client.get("/api/profiles/me")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "User profile"
    assert "profile" in body
    assert body["profile"]["username"] == os.getenv("USER_LOGIN")
    assert body["profile"]["role"]["name"] == "user"
    assert body["profile"]["is_active"] is True


def test_user_cannot_get_profile_without_token():
    client = ApiClient()

    response = client.get("/api/profiles/me")

    assert response.status_code in (401, 403)


def test_user_cannot_get_profile_with_invalid_token():
    client = ApiClient(token="invalid_token")

    response = client.get("/api/profiles/me")

    assert response.status_code in (401, 403)


def test_user_profile_response_has_required_fields(user_token):
    client = ApiClient(token=user_token)

    response = client.get("/api/profiles/me")

    assert response.status_code == 200

    profile = response.json()["profile"]

    assert "id" in profile
    assert "username" in profile
    assert "email" in profile
    assert "role" in profile
    assert "is_active" in profile


def test_user_can_get_profile_by_own_account_id(user_token):
    client = ApiClient(token=user_token)

    me_response = client.get("/api/profiles/me")

    assert me_response.status_code == 200

    account_id = me_response.json()["profile"]["id"]

    profile_response = client.get(f"/api/profiles/{account_id}")

    assert profile_response.status_code == 200

    body = profile_response.json()

    assert "profile" in body
    assert body["profile"]["id"] == account_id
    assert body["profile"]["username"] == os.getenv("USER_LOGIN")