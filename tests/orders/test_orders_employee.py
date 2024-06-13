def test_orders_create_employee(employee_client):
    response = employee_client.post("/orders/create", json={"name": "Test"})
    assert response.status_code == 403


def test_orders_read_employee(employee_client):
    response = employee_client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_orders_update_employee(employee_client):
    response = employee_client.patch("/orders/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_orders_delete_employee(employee_client):
    response = employee_client.delete("/orders/delete/1")
    assert response.status_code == 403
