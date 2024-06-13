def test_services_read_guest(guest_client):
    response = guest_client.get("/services/")
    assert response.status_code == 401


def test_services_create_guest(guest_client):
    response = guest_client.post("/services/create", json={"name": "Test", "minPrice": 1000, "minTime": 3600})
    assert response.status_code == 401


def test_services_update_guest(guest_client):
    response = guest_client.patch("/services/update/1", json={"name": "Test"})
    assert response.status_code == 401


def test_services_delete_guest(guest_client):
    response = guest_client.delete("/services/delete/1")
    assert response.status_code == 401
