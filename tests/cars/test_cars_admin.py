def test_cars_create_admin(admin_client):
    response = admin_client.post("/cars/create", json={"model": "Test", "brand_id": 1})
    assert response.status_code == 200
    assert response.json() == {'id': 17, 'model': 'Test', 'brand': {'id': 1, 'name': 'Pagani'}}


def test_cars_read_admin(admin_client):
    response = admin_client.get("/cars/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 17


def test_cars_read_admin_filter_id(admin_client):
    response = admin_client.get("/cars/?id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_cars_read_admin_filter_id_in(admin_client):
    response = admin_client.get("/cars/?id_in=1&id_in=2&id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["id"] == 2
    assert response.json()[2]["id"] == 3


def test_cars_read_admin_filter_model(admin_client):
    response = admin_client.get("/cars/?model=Test")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["model"] == "Test"


def test_cars_read_admin_filter_model_in(admin_client):
    response = admin_client.get("/cars/?model_in=Test&model_in=911&model_in=Test2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["model"] == "911"
    assert response.json()[1]["model"] == "Test"


def test_cars_read_admin_filter_brand_id(admin_client):
    response = admin_client.get("/cars/?brand_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["brand"]["id"] == 1
    assert response.json()[1]["brand"]["id"] == 1
    assert response.json()[2]["brand"]["id"] == 1


def test_cars_read_admin_filter_brand_id_in(admin_client):
    response = admin_client.get("/cars/?brand_id_in=1&brand_id_in=2&brand_id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["brand"]["id"] == 1
    assert response.json()[1]["brand"]["id"] == 1
    assert response.json()[2]["brand"]["id"] == 2
    assert response.json()[3]["brand"]["id"] == 2
    assert response.json()[4]["brand"]["id"] == 3


# brand name
def test_cars_read_admin_filter_brand_name(admin_client):
    response = admin_client.get("/cars/?brand_name=Pagani")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["brand"]["name"] == "Pagani"
    assert response.json()[1]["brand"]["name"] == "Pagani"
    assert response.json()[2]["brand"]["name"] == "Pagani"


def test_cars_read_admin_filter_brand_name_in(admin_client):
    response = admin_client.get("/cars/?brand_name_in=Pagani&brand_name_in=Ferrari&brand_name_in=Lamborghini")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["brand"]["name"] == "Pagani"
    assert response.json()[1]["brand"]["name"] == "Pagani"
    assert response.json()[2]["brand"]["name"] == "Ferrari"
    assert response.json()[3]["brand"]["name"] == "Ferrari"
    assert response.json()[4]["brand"]["name"] == "Lamborghini"


def test_cars_read_admin_sorted_id_asc(admin_client):
    response = admin_client.get("/cars/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_cars_read_admin_sorted_id_desc(admin_client):
    response = admin_client.get("/cars/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 17


def test_cars_read_admin_sorted_model_asc(admin_client):
    response = admin_client.get("/cars/?order_field=model&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 3


def test_cars_read_admin_sorted_model_desc(admin_client):
    response = admin_client.get("/cars/?order_field=model&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2


def test_cars_read_admin_sorted_brand_id_asc(admin_client):
    response = admin_client.get("/cars/?order_field=brand_id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["brand"]["id"] == 1


def test_cars_read_admin_sorted_brand_id_desc(admin_client):
    response = admin_client.get("/cars/?order_field=brand_id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["brand"]["id"] == 8


def test_cars_read_admin_sorted_incorrect_field(admin_client):
    response = admin_client.get("/cars/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_cars_read_admin_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/cars/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_cars_read_admin_limit(admin_client):
    response = admin_client.get("/cars/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_cars_read_admin_limit_negative(admin_client):
    response = admin_client.get("/cars/?limit=-1")
    assert response.status_code == 422


def test_cars_read_admin_limit_zero(admin_client):
    response = admin_client.get("/cars/?limit=0")
    assert response.status_code == 422


def test_cars_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/cars/?limit=incorrect")
    assert response.status_code == 422


def test_cars_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/cars/?limit=10000")
    assert response.status_code == 422


def test_cars_read_admin_offset(admin_client):
    response = admin_client.get("/cars/?offset=1&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 16


def test_cars_read_admin_offset_negative(admin_client):
    response = admin_client.get("/cars/?offset=-1")
    assert response.status_code == 422


def test_cars_read_admin_offset_zero(admin_client):
    response = admin_client.get("/cars/?offset=0&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 17


def test_cars_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/cars/?offset=incorrect")
    assert response.status_code == 422


def test_cars_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/cars/?offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_cars_update_admin(admin_client):
    response = admin_client.patch("/cars/update/17", json={"model": "Test2"})
    assert response.status_code == 200
    assert response.json() == {'id': 17, 'model': 'Test2', 'brand': {'id': 1, 'name': 'Pagani'}}


def test_cars_update_admin_incorrect_brand_id(admin_client):
    response = admin_client.patch("/cars/update/incorrect", json={"brand_id": 100})
    assert response.status_code == 422


def test_cars_update_admin_not_found_brand_id(admin_client):
    response = admin_client.patch("/cars/update/100", json={"brand_id": 100})
    assert response.status_code == 404


def test_cars_delete_admin(admin_client):
    response = admin_client.delete("/cars/delete/17")
    assert response.status_code == 200


def test_cars_delete_incorrect_id(admin_client):
    response = admin_client.delete("/cars/delete/incorrect")
    assert response.status_code == 422


def test_cars_delete_admin_not_found(admin_client):
    response = admin_client.delete("/cars/delete/100")
    assert response.status_code == 404


def test_cars_delete_admin_deleted(admin_client):
    response = admin_client.delete("/cars/delete/17")
    assert response.status_code == 404