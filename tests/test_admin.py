import pytest
from api_client import ApiClient

def safe_json(response):
    try:
        return response.json()
    except ValueError:
        pytest.fail(f"Ответ не является JSON: {response.text}")

def test_admin_can_get_own_profile(admin_token):
    client = ApiClient(token=admin_token)
    response = client.get("/api/profiles/me")
    assert response.status_code == 200
    body = safe_json(response)
    assert body["profile"]["role"]["name"] == "admin"

def test_admin_can_get_profiles_list(admin_token):
    client = ApiClient(token=admin_token)
    response = client.get("/api/profiles/")
    assert response.status_code == 200
    body = safe_json(response)
    assert isinstance(body, dict)

@pytest.mark.parametrize("role_fixture, expected_status", [
    ("admin_token", 200),
    ("moderator_token", 200),
    ("user_token", 200),
])
def test_profiles_list_access_by_role(role_fixture, expected_status, request):
    token = request.getfixturevalue(role_fixture)
    client = ApiClient(token=token)
    response = client.get("/api/profiles/")
    assert response.status_code == expected_status
    if expected_status != 200:
        body = safe_json(response)
        assert "detail" in body

def test_profiles_list_without_token_is_forbidden():
    client = ApiClient()
    response = client.get("/api/profiles/")

    assert response.status_code == 403
    body = safe_json(response)
    assert "detail" in body

def test_profiles_list_with_invalid_token_is_forbidden():
    client = ApiClient(token="invalid_token")
    response = client.get("/api/profiles/")
    assert response.status_code == 401
    body = safe_json(response)
    assert "detail" in body

def test_admin_can_get_user_profile_by_account_id(user_token, admin_token):
    user_client = ApiClient(token=user_token)
    me_response = user_client.get("/api/profiles/me")
    assert me_response.status_code == 200
    user_account_id = safe_json(me_response)["profile"]["id"]

    admin_client = ApiClient(token=admin_token)
    response = admin_client.get(f"/api/profiles/{user_account_id}")
    assert response.status_code == 200
    body = safe_json(response)
    assert body["profile"]["id"] == user_account_id

def test_user_cannot_get_admin_profile_by_account_id(user_token, admin_token):
    admin_client = ApiClient(token=admin_token)
    admin_me_response = admin_client.get("/api/profiles/me")
    assert admin_me_response.status_code == 200
    admin_account_id = safe_json(admin_me_response)["profile"]["id"]

    user_client = ApiClient(token=user_token)
    response = user_client.get(f"/api/profiles/{admin_account_id}")
    assert response.status_code == 403
    body = safe_json(response)
    assert "detail" in body