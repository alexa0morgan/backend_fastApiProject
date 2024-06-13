from models.order_model import Status


def test_orders_create_customer(customer_client):
    response = customer_client.post("/orders/create", json={"name": "Test"})
    assert response.status_code == 403


def test_orders_read_customer(customer_client):
    response = customer_client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_orders_read_customer_filter_id(customer_client):
    response = customer_client.get("/orders/?id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_filter_id_in(customer_client):
    response = customer_client.get("/orders/?id_in=1&id_in=2&id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_filter_customer_car_id(customer_client):
    response = customer_client.get("/orders/?customer_car_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["id"] == 1


def test_orders_read_customer_filter_customer_car_id_in(customer_client):
    response = customer_client.get("/orders/?customer_car_id_in=1&customer_car_id_in=2&customer_car_id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["id"] == 1


def test_orders_read_customer_filter_customer_car_year(customer_client):
    response = customer_client.get("/orders/?customer_car_year=2010")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["year"] == 2010


def test_orders_read_customer_filter_customer_car_year_gt(customer_client):
    response = customer_client.get("/orders/?customer_car_year_gt=2009")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["year"] == 2010


def test_orders_read_customer_filter_customer_car_year_lt(customer_client):
    response = customer_client.get("/orders/?customer_car_year_lt=2021")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["year"] == 2010


def test_orders_read_customer_car_license_plate(customer_client):
    response = customer_client.get("/orders/?customer_car_license_plate=A123AA")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["license_plate"] == "A123AA"


def test_orders_read_customer_filter_customer_id(customer_client):
    response = customer_client.get("/orders/?customer_id=5")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["customer"]["id"] == 5


def test_orders_read_customer_filter_customer_id_of_others(customer_client):
    response = customer_client.get("/orders/?customer_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_orders_read_customer_filter_customer_id_in(customer_client):
    response = customer_client.get("/orders/?customer_id_in=5&customer_id_in=6&customer_id_in=7")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_car"]["customer"]["id"] == 5


def test_orders_read_customer_filter_administrator_id(customer_client):
    response = customer_client.get("/orders/?administrator_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["administrator"]["id"] == 1


def test_orders_read_customer_filter_administrator_id_in(customer_client):
    response = customer_client.get("/orders/?administrator_id_in=1&administrator_id_in=2&administrator_id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["administrator"]["id"] == 1


# employee id
def test_orders_read_customer_filter_employee_id(customer_client):
    response = customer_client.get("/orders/?employee_id=2")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["employee"]["id"] == 2


def test_orders_read_customer_filter_employee_id_in(customer_client):
    response = customer_client.get("/orders/?employee_id_in=1&employee_id_in=2&employee_id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["employee"]["id"] == 2


def test_orders_read_customer_filter_status(customer_client):
    response = customer_client.get("/orders/?status=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == 1


def test_orders_read_customer_filter_status_not(customer_client):
    response = customer_client.get("/orders/?status=2")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_orders_read_customer_filter_start_date_gte(customer_client):
    response = customer_client.get("/orders/?start_date_gte=2020-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["start_date"] == "2021-10-01T12:00:00Z"


def test_orders_read_customer_filter_start_date_lte(customer_client):
    response = customer_client.get("/orders/?start_date_lte=2021-12-12")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["start_date"] == "2021-10-01T12:00:00Z"


def test_orders_read_customer_filter_end_date_gte(customer_client):
    response = customer_client.get("/orders/?end_date_gte=2020-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["end_date"] == "2021-10-01T15:00:00Z"


def test_orders_read_customer_filter_end_date_lte(customer_client):
    response = customer_client.get("/orders/?end_date_lte=2021-12-12")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["end_date"] == "2021-10-01T15:00:00Z"


def test_orders_read_customer_sorted_id_asc(customer_client):
    response = customer_client.get("/orders/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_id_desc(customer_client):
    response = customer_client.get("/orders/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_start_date_asc(customer_client):
    response = customer_client.get("/orders/?order_field=start_date&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_start_date_desc(customer_client):
    response = customer_client.get("/orders/?order_field=start_date&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_end_date_asc(customer_client):
    response = customer_client.get("/orders/?order_field=start_date&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_end_date_desc(customer_client):
    response = customer_client.get("/orders/?order_field=start_date&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_customer_sorted_incorrect_field(customer_client):
    response = customer_client.get("/orders/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_orders_read_customer_sorted_incorrect_direction(customer_client):
    response = customer_client.get("/orders/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_orders_read_customer_limit(customer_client):
    response = customer_client.get("/orders/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_orders_read_customer_limit_negative(customer_client):
    response = customer_client.get("/orders/?limit=-1")
    assert response.status_code == 422


def test_orders_read_customer_limit_zero(customer_client):
    response = customer_client.get("/orders/?limit=0")
    assert response.status_code == 422


def test_orders_read_customer_limit_incorrect(customer_client):
    response = customer_client.get("/orders/?limit=incorrect")
    assert response.status_code == 422


def test_orders_read_customer_limit_too_large(customer_client):
    response = customer_client.get("/orders/?limit=10000")
    assert response.status_code == 422


def test_orders_read_customer_offset(customer_client):
    response = customer_client.get("/orders/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) != 1


def test_orders_read_customer_offset_negative(customer_client):
    response = customer_client.get("/orders/?limit=100&offset=-1")
    assert response.status_code == 422


def test_orders_read_customer_offset_zero(customer_client):
    response = customer_client.get("/orders/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_orders_read_customer_offset_incorrect(customer_client):
    response = customer_client.get("/orders/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_orders_read_customer_offset_too_large(customer_client):
    response = customer_client.get("/orders/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_orders_update_customer(customer_client):
    response = customer_client.patch("/orders/update/1", json={"name": "Test"})
    assert response.status_code == 403


def test_orders_delete_customer(customer_client):
    response = customer_client.delete("/orders/delete/1")
    assert response.status_code == 403
