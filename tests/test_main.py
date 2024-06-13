def test_root(guest_client):
    response = guest_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
