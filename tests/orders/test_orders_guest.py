def test_orders_read_guest(guest_client):
    response = guest_client.get("/orders/")
    assert response.status_code == 401


def test_orders_create_guest(guest_client):
    response = guest_client.post("/orders/create", json={"name": "Test"})
    assert response.status_code == 401


def test_orders_update_guest(guest_client):
    response = guest_client.patch("/orders/update/1", json={"name": "Test"})
    assert response.status_code == 401


def test_orders_delete_guest(guest_client):
    response = guest_client.delete("/orders/delete/1")
    assert response.status_code == 401
