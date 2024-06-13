def test_users_me_guest(guest_client):
    response = guest_client.get("/users/me")
    assert response.status_code == 401


def test_users_create_guest(guest_client):
    response = guest_client.post("/users/create")
    assert response.status_code == 401


def test_users_read_guest(guest_client):
    response = guest_client.get("/users/")
    assert response.status_code == 401


def test_users_update_guest(guest_client):
    response = guest_client.patch("/users/update/1")
    assert response.status_code == 401


def test_users_delete_guest(guest_client):
    response = guest_client.delete("/users/delete/1")
    assert response.status_code == 401
