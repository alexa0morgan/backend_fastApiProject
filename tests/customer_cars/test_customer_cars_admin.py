def test_customer_cars_create_admin(admin_client):
    response = admin_client.post("/customer_cars/create", json={
        "car_id": 2,
        "customer_id": 1,
        "year": 2030,
        "license_plate": "A123AB"
    })
    assert response.status_code == 200
    assert response.json() == {
        'car': {
            'brand': {'id': 1, 'name': 'Pagani'},
            'id': 2,
            'model': 'Zonda'
        },
        'car_id': 2,
        'customer': {
            'email': 'jdoe@example.com',
            'full_name': 'John Doe Smith',
            'id': 1
        },
        'id': 3,
        'license_plate': 'A123AB',
        'year': 2030
    }


def test_customer_cars_read_admin(admin_client):
    response = admin_client.get("/customer_cars/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_customer_cars_read_admin_filter_id(admin_client):
    response = admin_client.get("/customer_cars/?id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_customer_cars_read_admin_filter_id_not_found(admin_client):
    response = admin_client.get("/customer_cars/?id=1000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_id_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?id=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_filter_id_in(admin_client):
    response = admin_client.get("/customer_cars/?id_in=1&id_in=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_filter_car_id(admin_client):
    response = admin_client.get("/customer_cars/?car_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["car_id"] == 1


def test_customer_cars_read_admin_filter_car_id_not_found(admin_client):
    response = admin_client.get("/customer_cars/?car_id=1000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_car_id_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?car_id=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_filter_car_id_in(admin_client):
    response = admin_client.get("/customer_cars/?car_id_in=1&car_id_in=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_filter_customer_id(admin_client):
    response = admin_client.get("/customer_cars/?customer_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer"]["id"] == 1


def test_customer_cars_read_admin_filter_customer_id_not_found(admin_client):
    response = admin_client.get("/customer_cars/?customer_id=1000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_customer_id_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?customer_id=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_filter_customer_id_in(admin_client):
    response = admin_client.get("/customer_cars/?customer_id_in=1&customer_id_in=2")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_customer_cars_read_admin_filter_year(admin_client):
    response = admin_client.get("/customer_cars/?year=2020")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["year"] == 2020


def test_customer_cars_read_admin_filter_year_not_found(admin_client):
    response = admin_client.get("/customer_cars/?year=1000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_year_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?year=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_filter_year_in(admin_client):
    response = admin_client.get("/customer_cars/?year_in=2020&year_in=2010")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_filter_year_gt(admin_client):
    response = admin_client.get("/customer_cars/?year_gt=2015")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_filter_year_lt(admin_client):
    response = admin_client.get("/customer_cars/?year_lt=2014")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_customer_cars_read_admin_filter_license_plate(admin_client):
    response = admin_client.get("/customer_cars/?license_plate=A123AA")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["license_plate"] == "A123AA"


def test_customer_cars_read_admin_filter_license_plate_not_found(admin_client):
    response = admin_client.get("/customer_cars/?license_plate=NTFND")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_license_plate_in(admin_client):
    response = admin_client.get("/customer_cars/?license_plate_in=A123AA&license_plate_in=B456BB")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_filter_customer_first_name(admin_client):
    response = admin_client.get("/customer_cars/?customer_first_name=Bob")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "Bob" in response.json()[0]["customer"]["full_name"]


def test_customer_cars_read_admin_filter_customer_first_name_not_found(admin_client):
    response = admin_client.get("/customer_cars/?customer_first_name=NTFND")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_customer_first_name_in(admin_client):
    response = admin_client.get("/customer_cars/?customer_first_name_in=Bob&customer_first_name_in=Alex")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_customer_cars_read_admin_filter_customer_last_name(admin_client):
    response = admin_client.get("/customer_cars/?customer_last_name=Brown")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "Brown" in response.json()[0]["customer"]["full_name"]


def test_customer_cars_read_admin_filter_customer_last_name_not_found(admin_client):
    response = admin_client.get("/customer_cars/?customer_last_name=NTFND")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_customer_last_name_in(admin_client):
    response = admin_client.get("/customer_cars/?customer_last_name_in=Brown&customer_last_name_in=Johnson")
    assert response.status_code == 200
    assert len(response.json()) == 1


# car model
def test_customer_cars_read_admin_filter_car_model(admin_client):
    response = admin_client.get("/customer_cars/?car_model=Huayra")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["car"]["model"] == "Huayra"


def test_customer_cars_read_admin_filter_car_model_not_found(admin_client):
    response = admin_client.get("/customer_cars/?car_model=NTFND")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_read_admin_filter_car_model_in(admin_client):
    response = admin_client.get("/customer_cars/?car_model_in=Huayra&car_model_in=488 GTB&car_model_in=Test")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cars_read_admin_sorted_id_asc(admin_client):
    response = admin_client.get("/customer_cars/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_customer_cars_read_admin_sorted_id_desc(admin_client):
    response = admin_client.get("/customer_cars/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 3


def test_customer_cars_read_admin_sorted_incorrect_field(admin_client):
    response = admin_client.get("/customer_cars/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_customer_cars_read_admin_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/customer_cars/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_limit(admin_client):
    response = admin_client.get("/customer_cars/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_customer_cars_read_admin_limit_negative(admin_client):
    response = admin_client.get("/customer_cars/?limit=-1")
    assert response.status_code == 422


def test_customer_cars_read_admin_limit_zero(admin_client):
    response = admin_client.get("/customer_cars/?limit=0")
    assert response.status_code == 422


def test_customer_cars_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?limit=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/customer_cars/?limit=10000")
    assert response.status_code == 422


def test_customer_cars_read_admin_offset(admin_client):
    response = admin_client.get("/customer_cars/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) != 1


def test_customer_cars_read_admin_offset_negative(admin_client):
    response = admin_client.get("/customer_cars/?limit=100&offset=-1")
    assert response.status_code == 422


def test_customer_cars_read_admin_offset_zero(admin_client):
    response = admin_client.get("/customer_cars/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_customer_cars_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/customer_cars/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_customer_cars_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/customer_cars/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_customer_cars_update_admin(admin_client):
    response = admin_client.patch("/customer_cars/update/3", json={"name": "Test2"})
    assert response.status_code == 200
    assert response.json() == {
        'car_id': 2,
        'year': 2030,
        'license_plate': 'A123AB',
        'id': 3,
        'customer': {
            'id': 1,
            'email': 'jdoe@example.com',
            'full_name': 'John Doe Smith'
        },
        'car': {
            'model': 'Zonda',
            'id': 2,
            'brand': {
                'name': 'Pagani',
                'id': 1
            }
        }
    }


def test_customer_cars_update_admin_incorrect_id(admin_client):
    response = admin_client.patch("/customer_cars/update/incorrect", json={"name": "Test2"})
    assert response.status_code == 422


def test_customer_cars_update_admin_not_found_id(admin_client):
    response = admin_client.patch("/customer_cars/update/1000", json={"name": "Test2"})
    assert response.status_code == 404


def test_customer_cars_delete_admin(admin_client):
    response = admin_client.delete("/customer_cars/delete/1")
    assert response.status_code == 200


def test_customer_cars_delete_admin_incorrect_id(admin_client):
    response = admin_client.delete("/customer_cars/delete/incorrect")
    assert response.status_code == 422


def test_customer_cars_delete_admin_not_found_id(admin_client):
    response = admin_client.delete("/customer_cars/delete/1000")
    assert response.status_code == 404


def test_customer_cars_delete_admin_deleted_id(admin_client):
    response = admin_client.delete("/customer_cars/delete/1")
    assert response.status_code == 404
