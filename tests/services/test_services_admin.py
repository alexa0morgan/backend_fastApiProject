def test_services_create_admin(admin_client):
    response = admin_client.post("/services/create", json={"name": "Test", "minPrice": 1000, "minTime": 3600})
    assert response.status_code == 200
    assert response.json() == {
        'id': 6,
        'name': 'Test',
        'price': {'cents': 1000, 'formatted': '10 руб. 0 коп.', 'rubles': 10},
        'time': {'minutes': 60, 'seconds': 3600}
    }


def test_services_read_admin(admin_client):
    response = admin_client.get("/services/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_services_read_admin_sorted_incorrect_field(admin_client):
    response = admin_client.get("/services/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_services_read_admin_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/services/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_services_read_admin_limit(admin_client):
    response = admin_client.get("/services/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_services_read_admin_limit_negative(admin_client):
    response = admin_client.get("/services/?limit=-1")
    assert response.status_code == 422


def test_services_read_admin_limit_zero(admin_client):
    response = admin_client.get("/services/?limit=0")
    assert response.status_code == 422


def test_services_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/services/?limit=incorrect")
    assert response.status_code == 422


def test_services_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/services/?limit=10000")
    assert response.status_code == 422


def test_services_read_admin_offset(admin_client):
    response = admin_client.get("/services/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_services_read_admin_offset_negative(admin_client):
    response = admin_client.get("/services/?limit=100&offset=-1")
    assert response.status_code == 422


def test_services_read_admin_offset_zero(admin_client):
    response = admin_client.get("/services/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_services_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/services/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_services_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/services/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_services_update_admin(admin_client):
    response = admin_client.patch("/services/update/6", json={"name": "Test2"})
    assert response.status_code == 200
    assert response.json() == {
        'id': 6,
        'name': 'Test2',
        'price': {'cents': 1000, 'formatted': '10 руб. 0 коп.', 'rubles': 10},
        'time': {'minutes': 60, 'seconds': 3600}
    }


def test_services_update_admin_incorrect_id(admin_client):
    response = admin_client.patch("/services/update/incorrect", json={"name": "Test2"})
    assert response.status_code == 422


def test_services_update_admin_not_found_id(admin_client):
    response = admin_client.patch("/services/update/1000", json={"name": "Test2"})
    assert response.status_code == 404


def test_services_delete_admin(admin_client):
    response = admin_client.delete("/services/delete/1")
    assert response.status_code == 200


def test_services_delete_admin_incorrect_id(admin_client):
    response = admin_client.delete("/services/delete/incorrect")
    assert response.status_code == 422


def test_services_delete_admin_not_found(admin_client):
    response = admin_client.delete("/services/delete/1000")
    assert response.status_code == 404


def test_services_delete_admin_deleted(admin_client):
    response = admin_client.delete("/services/delete/1")
    assert response.status_code == 404