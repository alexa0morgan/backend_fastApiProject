def test_customer_cars_read_customer(customer_client):
    response = customer_client.get("/customer_cars/")
    assert response.status_code == 403


def test_customer_cars_create_customer(customer_client):
    response = customer_client.post("/customer_cars/create", json={"name": "Test"})
    assert response.status_code == 403


def test_customer_cars_update_customer(customer_client):
    response = customer_client.patch("/customer_cars/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_customer_cars_delete_customer(customer_client):
    response = customer_client.delete("/customer_cars/delete/1")
    assert response.status_code == 403
