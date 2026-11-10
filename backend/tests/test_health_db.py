def test_health_db_shape(client):
    response = client.get("/health/db")
    assert response.status_code in (200, 503)
    payload = response.json()
    assert "success" in payload
    assert "message" in payload

