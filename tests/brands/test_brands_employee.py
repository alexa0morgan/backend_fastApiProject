def test_brands_read_employee(employee_client):
    response = employee_client.get("/brands/")
    assert response.status_code == 403


def test_brands_create_employee(employee_client):
    response = employee_client.post("/brands/create", json={"name": "Test"})
    assert response.status_code == 403


def test_brands_update_employee(employee_client):
    response = employee_client.patch("/brands/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_brands_delete_employee(employee_client):
    response = employee_client.delete("/brands/delete/1")
    assert response.status_code == 403
