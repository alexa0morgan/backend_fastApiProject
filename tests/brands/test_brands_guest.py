def test_brands_read_guest(guest_client):
    response = guest_client.get("/brands/")
    assert response.status_code == 401


def test_brands_create_guest(guest_client):
    response = guest_client.post("/brands/create", json={"name": "Test"})
    assert response.status_code == 401


def test_brands_update_guest(guest_client):
    response = guest_client.patch("/brands/update/1", json={"name": "Test"})
    assert response.status_code == 401


def test_brands_delete_guest(guest_client):
    response = guest_client.delete("/brands/delete/1")
    assert response.status_code == 401
