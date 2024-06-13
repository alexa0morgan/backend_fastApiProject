def test_services_read_employee(employee_client):
    response = employee_client.get("/services/")
    assert response.status_code == 403


def test_services_create_employee(employee_client):
    response = employee_client.post("/services/create", json={"name": "Test", "minPrice": 1000, "minTime": 3600})
    assert response.status_code == 403


def test_services_update_employee(employee_client):
    response = employee_client.patch("/services/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_services_delete_employee(employee_client):
    response = employee_client.delete("/services/delete/1")
    assert response.status_code == 403
