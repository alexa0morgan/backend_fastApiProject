def test_users_admin_me(admin_client):
    response = admin_client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {
        "email": "jdoe@example.com",
        "first_name": "John",
        "id": 1,
        "last_name": "Doe",
        "patronymic": "Smith",
        "role_id": 1,
        "send_notifications": True
    }


def test_users_admin_create(admin_client):
    response = admin_client.post(
        "/users/create",
        json={
            "email": "nonexistent@example.com",
            "first_name": "foobar",
            "last_name": "User",
            "role_id": 3,
            "send_notifications": False,
            "password": "password",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "email": "nonexistent@example.com",
        "first_name": "foobar",
        "id": 10,
        "last_name": "User",
        "patronymic": None,
        "role_id": 3,
        "send_notifications": False
    }


def test_users_admin_create_duplicate_email(admin_client):
    response = admin_client.post(
        "/users/create",
        json={
            "email": "jdoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role_id": 1,
            "send_notifications": True,
            "password": "password",
        },
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "User with this email already exists"}


def test_users_admin_read(admin_client):
    response = admin_client.get("/users/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 7


def test_users_admin_read_filters_role_id(admin_client):
    response = admin_client.get("/users/?role_id=1&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_users_admin_read_filters_id(admin_client):
    response = admin_client.get("/users/?id=5&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_admin_read_filters_id_in(admin_client):
    response = admin_client.get("/users/?id_in=1&id_in=2&id_in=3&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_users_admin_read_filters_first_name(admin_client):
    response = admin_client.get("/users/?first_name=o&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_users_admin_read_filters_first_name_in(admin_client):
    response = admin_client.get("/users/?first_name_in=John&first_name_in=Jane&first_name_in=Nonexistent&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_users_admin_read_filters_last_name(admin_client):
    response = admin_client.get("/users/?last_name=doe&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_users_admin_read_filters_last_name_in(admin_client):
    response = admin_client.get("/users/?last_name_in=Doe&last_name_in=Johnson&last_name_in=Nonexistent&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_users_admin_read_filters_email(admin_client):
    response = admin_client.get("/users/?email=example.com&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_users_admin_read_filters_send_notifications_true(admin_client):
    response = admin_client.get("/users/?send_notifications=true&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_users_admin_read_filters_send_notifications_false(admin_client):
    response = admin_client.get("/users/?send_notifications=false&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_users_admin_read_filters_patronymic(admin_client):
    response = admin_client.get("/users/?patronymic=smith&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_admin_read_filters_patronymic_in(admin_client):
    response = admin_client.get("/users/?patronymic_in=Smith&patronymic_in=Johnson&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_admin_read_limit(admin_client):
    response = admin_client.get("/users/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_admin_read_offset(admin_client):
    response = admin_client.get("/users/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_users_admin_read_sorted_id_asc(admin_client):
    response = admin_client.get("/users/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_users_admin_read_sorted_id_desc(admin_client):
    response = admin_client.get("/users/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] != 1


def test_users_admin_read_sorted_first_name_asc(admin_client):
    response = admin_client.get("/users/?order_field=first_name&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 4


def test_users_admin_read_sorted_first_name_desc(admin_client):
    response = admin_client.get("/users/?order_field=first_name&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 10


def test_users_admin_read_sorted_last_name_asc(admin_client):
    response = admin_client.get("/users/?order_field=last_name&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 5


def test_users_admin_read_sorted_last_name_desc(admin_client):
    response = admin_client.get("/users/?order_field=last_name&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 6


def test_users_admin_read_sorted_patronymic_asc(admin_client):
    response = admin_client.get("/users/?order_field=patronymic&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2


def test_users_admin_read_sorted_patronymic_desc(admin_client):
    response = admin_client.get("/users/?order_field=patronymic&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_users_admin_read_sorted_email_asc(admin_client):
    response = admin_client.get("/users/?order_field=email&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 4


def test_users_admin_read_sorted_email_desc(admin_client):
    response = admin_client.get("/users/?order_field=email&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 10


def test_users_admin_read_sorted_role_id_asc(admin_client):
    response = admin_client.get("/users/?order_field=role_id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_users_admin_read_sorted_role_id_desc(admin_client):
    response = admin_client.get("/users/?order_field=role_id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 3


def test_users_admin_read_sorted_incorrect_field(admin_client):
    response = admin_client.get("/users/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_users_admin_read_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/users/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_users_read_admin_limit(admin_client):
    response = admin_client.get("/users/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_users_read_admin_limit_negative(admin_client):
    response = admin_client.get("/users/?limit=-1")
    assert response.status_code == 422


def test_users_read_admin_limit_zero(admin_client):
    response = admin_client.get("/users/?limit=0")
    assert response.status_code == 422


def test_users_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/users/?limit=incorrect")
    assert response.status_code == 422


def test_users_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/users/?limit=10000")
    assert response.status_code == 422


def test_users_read_admin_offset(admin_client):
    response = admin_client.get("/users/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) != 1


def test_users_read_admin_offset_negative(admin_client):
    response = admin_client.get("/users/?limit=100&offset=-5")
    assert response.status_code == 422


def test_users_read_admin_offset_zero(admin_client):
    response = admin_client.get("/users/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 7


def test_users_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/users/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_users_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/users/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_users_admin_update(admin_client):
    response = admin_client.patch(
        "/users/update/1",
        json={"last_name": "Jones"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "email": "jdoe@example.com",
        "first_name": "John",
        "id": 1,
        "last_name": "Jones",
        "patronymic": "Smith",
        "role_id": 1,
        "send_notifications": True
    }


def test_users_admin_update_incorrect_id(admin_client):
    response = admin_client.patch(
        "/users/update/incorrect",
        json={"last_name": "Jones"},
    )
    assert response.status_code == 422


def test_users_admin_update_not_found(admin_client):
    response = admin_client.patch(
        "/users/update/100",
        json={"last_name": "Jones"},
    )
    assert response.status_code == 404


def test_users_admin_delete(admin_client):
    response = admin_client.delete("/users/delete/6")
    assert response.status_code == 200


def test_users_admin_delete_incorrect_id(admin_client):
    response = admin_client.delete("/users/delete/incorrect")
    assert response.status_code == 422


def test_users_admin_delete_not_found(admin_client):
    response = admin_client.delete("/users/delete/100")
    assert response.status_code == 404


def test_users_admin_delete_deleted(admin_client):
    response = admin_client.delete("/users/delete/6")
    assert response.status_code == 404
