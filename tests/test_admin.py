from api_client import ApiClient


def test_admin_can_get_own_profile(admin_token):
    client = ApiClient(token=admin_token)

    response = client.get("/api/profiles/me")

    assert response.status_code == 200
    assert response.json()["profile"]["role"]["name"] == "admin"


def test_admin_can_get_profiles_list(admin_token):
    client = ApiClient(token=admin_token)

    response = client.get("/api/profiles/")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_profiles_list_without_token_is_forbidden():
    client = ApiClient()

    response = client.get("/api/profiles/")

    assert response.status_code in (401, 403)


def test_profiles_list_with_invalid_token_is_forbidden():
    client = ApiClient(token="invalid_token")

    response = client.get("/api/profiles/")

    assert response.status_code in (401, 403)


def test_admin_can_get_user_profile_by_account_id(user_token, admin_token):
    user_client = ApiClient(token=user_token)

    me_response = user_client.get("/api/profiles/me")

    assert me_response.status_code == 200

    user_account_id = me_response.json()["profile"]["id"]

    admin_client = ApiClient(token=admin_token)

    response = admin_client.get(f"/api/profiles/{user_account_id}")

    assert response.status_code == 200
    assert response.json()["profile"]["id"] == user_account_id


def test_user_cannot_get_admin_profile_by_account_id(user_token, admin_token):
    admin_client = ApiClient(token=admin_token)

    admin_me_response = admin_client.get("/api/profiles/me")

    assert admin_me_response.status_code == 200

    admin_account_id = admin_me_response.json()["profile"]["id"]

    user_client = ApiClient(token=user_token)

    response = user_client.get(f"/api/profiles/{admin_account_id}")

    assert response.status_code in (403, 404)