def test_permissions_pagination_and_search(client, admin_auth_headers):
    for code in ["billing.read", "billing.write", "inventory.read", "inventory.write"]:
        client.post(
            "/api/v1/iam/permissions",
            headers=admin_auth_headers,
            json={"code": code, "description": f"{code} permission"},
        )

    page_one = client.get(
        "/api/v1/iam/permissions?page=1&page_size=2",
        headers=admin_auth_headers,
    )
    assert page_one.status_code == 200
    page_one_payload = page_one.json()
    assert page_one_payload["meta"]["page"] == 1
    assert page_one_payload["meta"]["page_size"] == 2
    assert page_one_payload["meta"]["total"] >= 6
    assert len(page_one_payload["data"]) == 2

    search_response = client.get(
        "/api/v1/iam/permissions?q=billing",
        headers=admin_auth_headers,
    )
    assert search_response.status_code == 200
    search_payload = search_response.json()
    assert all("billing" in item["code"] for item in search_payload["data"])


def test_users_filter_active_state(client, admin_auth_headers):
    users_response = client.get("/api/v1/iam/users", headers=admin_auth_headers)
    assert users_response.status_code == 200
    users = users_response.json()["data"]
    viewer_id = next(user["id"] for user in users if user["username"] == "viewer")

    toggle_response = client.patch(
        f"/api/v1/iam/users/{viewer_id}",
        headers=admin_auth_headers,
        json={"is_active": False},
    )
    assert toggle_response.status_code == 200

    inactive_response = client.get(
        "/api/v1/iam/users?is_active=false",
        headers=admin_auth_headers,
    )
    assert inactive_response.status_code == 200
    inactive_users = inactive_response.json()["data"]
    assert any(user["username"] == "viewer" for user in inactive_users)

