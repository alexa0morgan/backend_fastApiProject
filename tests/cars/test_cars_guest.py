def test_cars_read_guest(guest_client):
    response = guest_client.get("/cars/")
    assert response.status_code == 401


def test_cars_create_guest(guest_client):
    response = guest_client.post("/cars/create", json={"name": "Test", "brand_id": 1})
    assert response.status_code == 401


def test_cars_update_guest(guest_client):
    response = guest_client.patch("/cars/update/1", json={"name": "Test"})
    assert response.status_code == 401


def test_cars_delete_guest(guest_client):
    response = guest_client.delete("/cars/delete/1")
    assert response.status_code == 401
