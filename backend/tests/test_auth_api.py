def test_login_success_and_me(client, seed_auth_data):
    login_response = client.post("/api/v1/auth/login", json=seed_auth_data["admin"])
    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload["success"] is True
    assert login_payload["data"]["token_type"] == "bearer"

    token = login_payload["data"]["access_token"]
    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    me_payload = me_response.json()
    assert me_payload["data"]["email"] == seed_auth_data["admin"]["email"]
    assert "iam.manage" in me_payload["data"]["permissions"]


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401

