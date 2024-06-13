def test_customer_cars_read_guest(guest_client):
    response = guest_client.get("/customer_cars/")
    assert response.status_code == 401


def test_customer_cars_create_guest(guest_client):
    response = guest_client.post("/customer_cars/create", json={"name": "Test"})
    assert response.status_code == 401


def test_customer_cars_update_guest(guest_client):
    response = guest_client.patch("/customer_cars/update/1", json={"name": "Test"})
    assert response.status_code == 401


def test_customer_cars_delete_guest(guest_client):
    response = guest_client.delete("/customer_cars/delete/1")
    assert response.status_code == 401
