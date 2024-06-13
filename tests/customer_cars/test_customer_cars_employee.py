def test_customer_cars_read_employee(employee_client):
    response = employee_client.get("/customer_cars/")
    assert response.status_code == 403


def test_customer_cars_create_employee(employee_client):
    response = employee_client.post("/customer_cars/create", json={"name": "Test"})
    assert response.status_code == 403


def test_customer_cars_update_employee(employee_client):
    response = employee_client.patch("/customer_cars/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_customer_cars_delete_employee(employee_client):
    response = employee_client.delete("/customer_cars/delete/1")
    assert response.status_code == 403
