def test_brands_read_customer(customer_client):
    response = customer_client.get("/brands/")
    assert response.status_code == 403


def test_brands_create_customer(customer_client):
    response = customer_client.post("/brands/create", json={"name": "Test"})
    assert response.status_code == 403


def test_brands_update_customer(customer_client):
    response = customer_client.patch("/brands/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_brands_delete_customer(customer_client):
    response = customer_client.delete("/brands/delete/1")
    assert response.status_code == 403
