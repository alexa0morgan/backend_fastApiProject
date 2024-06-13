def test_cars_read_employee(employee_client):
    response = employee_client.get("/cars/")
    assert response.status_code == 403


def test_cars_create_employee(employee_client):
    response = employee_client.post("/cars/create", json={"name": "Test", "brand_id": 1})
    assert response.status_code == 403


def test_cars_update_employee(employee_client):
    response = employee_client.patch("/cars/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_cars_delete_employee(employee_client):
    response = employee_client.delete("/cars/delete/1")
    assert response.status_code == 403
