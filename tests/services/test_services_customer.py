def test_services_read_customer(customer_client):
    response = customer_client.get("/services/")
    assert response.status_code == 403


def test_services_create_customer(customer_client):
    response = customer_client.post("/services/create", json={"name": "Test", "minPrice": 1000, "minTime": 3600})
    assert response.status_code == 403


def test_services_update_customer(customer_client):
    response = customer_client.patch("/services/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_services_delete_customer(customer_client):
    response = customer_client.delete("/services/delete/1")
    assert response.status_code == 403
