def test_users_customer_me(customer_client):
    response = customer_client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "id": 5,
        "email": "bbrown@example.net",
        "first_name": "Bob",
        "last_name": "Brown",
        "patronymic": None,
        "role_id": 3,
        "send_notifications": False,
    }


def test_users_customer_create(customer_client):
    response = customer_client.post(
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


def test_users_customer_read(customer_client):
    response = customer_client.get("/users/")
    assert response.status_code == 403


def test_users_customer_update(customer_client):
    response = customer_client.patch(
        "/users/update/1",
        json={"first_name": "Alice", "last_name": "Johnson"},
    )
    assert response.status_code == 403


def test_users_customer_delete(customer_client):
    response = customer_client.delete("/users/delete/1")
    assert response.status_code == 403
