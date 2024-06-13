def test_brands_create_admin(admin_client):
    response = admin_client.post("/brands/create", json={"name": "Test"})
    assert response.status_code == 200
    assert response.json() == {'id': 9, 'name': 'Test'}


def test_brands_read_admin(admin_client):
    response = admin_client.get("/brands/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_brands_read_admin_filter_id(admin_client):
    response = admin_client.get("/brands/?id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_brands_read_admin_filter_id_in(admin_client):
    response = admin_client.get("/brands/?id_in=1&id_in=2&id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["id"] == 2
    assert response.json()[2]["id"] == 3


def test_brands_read_admin_filter_name(admin_client):
    response = admin_client.get("/brands/?name=Pagani")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Pagani"


def test_brands_read_admin_filter_name_in(admin_client):
    response = admin_client.get("/brands/?name_in=Pagani&name_in=Lamborghini&name_in=NTFND")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Pagani"
    assert response.json()[1]["name"] == "Lamborghini"


def test_brands_read_admin_sorted_id_asc(admin_client):
    response = admin_client.get("/brands/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_brands_read_admin_sorted_id_desc(admin_client):
    response = admin_client.get("/brands/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 9


def test_brands_read_admin_sorted_name_asc(admin_client):
    response = admin_client.get("/brands/?order_field=name&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 6


def test_brands_read_admin_sorted_name_desc(admin_client):
    response = admin_client.get("/brands/?order_field=name&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 9


def test_brands_read_admin_sorted_incorrect_field(admin_client):
    response = admin_client.get("/brands/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_brands_read_admin_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/brands/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_brands_read_admin_limit(admin_client):
    response = admin_client.get("/brands/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_brands_read_admin_limit_negative(admin_client):
    response = admin_client.get("/brands/?limit=-1")
    assert response.status_code == 422


def test_brands_read_admin_limit_zero(admin_client):
    response = admin_client.get("/brands/?limit=0")
    assert response.status_code == 422


def test_brands_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/brands/?limit=incorrect")
    assert response.status_code == 422


def test_brands_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/brands/?limit=10000")
    assert response.status_code == 422


def test_brands_read_admin_offset(admin_client):
    response = admin_client.get("/brands/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) != 1


def test_brands_read_admin_offset_negative(admin_client):
    response = admin_client.get("/brands/?limit=100&offset=-1")
    assert response.status_code == 422


def test_brands_read_admin_offset_zero(admin_client):
    response = admin_client.get("/brands/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_brands_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/brands/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_brands_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/brands/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_brands_update_admin(admin_client):
    response = admin_client.patch("/brands/update/9", json={"name": "Test2"})
    assert response.status_code == 200
    assert response.json() == {'id': 9, 'name': 'Test2'}


def test_brands_update_admin_incorrect_id(admin_client):
    response = admin_client.patch("/brands/update/incorrect", json={"name": "Test2"})
    assert response.status_code == 422


def test_brands_update_admin_not_found_id(admin_client):
    response = admin_client.patch("/brands/update/1000", json={"name": "Test2"})
    assert response.status_code == 404


def test_brands_delete_admin(admin_client):
    response = admin_client.delete("/brands/delete/1")
    assert response.status_code == 200


def test_brands_delete_admin_incorrect_id(admin_client):
    response = admin_client.delete("/brands/delete/incorrect")
    assert response.status_code == 422


def test_brands_delete_admin_not_found_id(admin_client):
    response = admin_client.delete("/brands/delete/1000")
    assert response.status_code == 404


def test_brands_delete_admin_deleted_id(admin_client):
    response = admin_client.delete("/brands/delete/1")
    assert response.status_code == 404
