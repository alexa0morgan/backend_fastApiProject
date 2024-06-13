def test_users_employee_me(employee_client):
    response = employee_client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "email": "ajonson@example.com",
        "first_name": "Alex",
        "id": 4,
        "last_name": "Johnson",
        "patronymic": None,
        "role_id": 2,
        "send_notifications": True
    }


def test_users_employee_create(employee_client):
    response = employee_client.post(
        "/users/create",
        json={
            "email": "nonexistent@example.com",
            "first_name": "Nonexistent",
            "last_name": "User",
            "role_id": 3,
            "send_notifications": False,
            "password": "password",
        },
    )

    assert response.status_code == 403


def test_users_employee_read(employee_client):
    response = employee_client.get("/users/")
    assert response.status_code == 403


def test_users_employee_update(employee_client):
    response = employee_client.patch(
        "/users/update/1",
        json={"first_name": "Alice", "last_name": "Johnson"},
    )
    assert response.status_code == 403


def test_users_employee_delete(employee_client):
    response = employee_client.delete("/users/delete/1")
    assert response.status_code == 403
