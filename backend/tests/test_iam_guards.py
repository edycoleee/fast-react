def test_access_summary_requires_access_read(client, viewer_auth_headers):
    response = client.get("/api/v1/access/summary", headers=viewer_auth_headers)
    assert response.status_code == 403


def test_iam_requires_manage_permission(client, viewer_auth_headers):
    response = client.get("/api/v1/iam/users", headers=viewer_auth_headers)
    assert response.status_code == 403


def test_admin_can_access_iam_endpoints(client, admin_auth_headers):
    list_response = client.get("/api/v1/iam/permissions", headers=admin_auth_headers)
    assert list_response.status_code == 200

    create_response = client.post(
        "/api/v1/iam/permissions",
        headers=admin_auth_headers,
        json={"code": "reports.read", "description": "read reports"},
    )
    assert create_response.status_code == 201

