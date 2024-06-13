def test_orders_create_admin(admin_client):
    response = admin_client.post("/orders/create", json={
        'administrator_id': 1,
        'employee_id': 2,
        'customer_car_id': 2,
        'services': [1, 2, 3],
    })
    assert response.status_code == 200
    json = response.json()
    assert response.json() == {
        'administrator': {
            'email': 'jdoe@example.com',
            'full_name': 'John Doe Smith',
            'id': 1
        },
        'customer_car': {
            'car': {'brand_name': 'Ferrari', 'model': '488 GTB'},
            'customer': {'email': 'cust@example.com', 'full_name': 'Customer2 User', 'id': 6},
            'id': 2,
            'license_plate': 'B456BB',
            'year': 2020
        },
        'employee': {'email': 'jadoe@example.com', 'full_name': 'Jane Doe', 'id': 2},
        'end_date': json['end_date'],
        'id': 5,
        'services': [
            {
                'id': 1,
                'name': 'Oil change',
                'price': {'cents': 200000, 'formatted': '2000 руб. 0 коп.', 'rubles': 2000},
                'time': {'minutes': 30, 'seconds': 1800}
            },
            {
                'id': 2,
                'name': 'Tire replacement',
                'price': {'cents': 500000, 'formatted': '5000 руб. 0 коп.', 'rubles': 5000},
                'time': {'minutes': 60, 'seconds': 3600}
            },
            {
                'id': 3,
                'name': 'Wheel alignment',
                'price': {'cents': 300000, 'formatted': '3000 руб. 0 коп.', 'rubles': 3000},
                'time': {'minutes': 40, 'seconds': 2400}
            }
        ],
        'start_date': json['start_date'],
        'status': 1,
        'total_price': 10000,
        'total_time': 130
    }


def test_orders_read_admin(admin_client):
    response = admin_client.get("/orders/?limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_orders_read_admin_filter_id(admin_client):
    response = admin_client.get("/orders/?id=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_orders_read_admin_filter_id_in(admin_client):
    response = admin_client.get("/orders/?id_in=1&id_in=2&id_in=3")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["id"] == 1
    assert response.json()[1]["id"] == 2
    assert response.json()[2]["id"] == 3


def test_orders_read_admin_sorted_id_asc(admin_client):
    response = admin_client.get("/orders/?order_field=id&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_admin_sorted_id_desc(admin_client):
    response = admin_client.get("/orders/?order_field=id&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 5


def test_orders_read_admin_sorted_start_date_asc(admin_client):
    response = admin_client.get("/orders/?order_field=start_date&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1


def test_orders_read_admin_sorted_start_date_desc(admin_client):
    response = admin_client.get("/orders/?order_field=start_date&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 5


def test_orders_read_admin_sorted_end_date_asc(admin_client):
    response = admin_client.get("/orders/?order_field=end_date&order_direction=asc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2


def test_orders_read_admin_sorted_end_date_desc(admin_client):
    response = admin_client.get("/orders/?order_field=end_date&order_direction=desc")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 5


def test_orders_read_admin_sorted_incorrect_field(admin_client):
    response = admin_client.get("/orders/?order_field=incorrect&order_direction=asc")
    assert response.status_code == 422


def test_orders_read_admin_sorted_incorrect_direction(admin_client):
    response = admin_client.get("/orders/?order_field=id&order_direction=incorrect")
    assert response.status_code == 422


def test_orders_read_admin_limit(admin_client):
    response = admin_client.get("/orders/?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_orders_read_admin_limit_negative(admin_client):
    response = admin_client.get("/orders/?limit=-1")
    assert response.status_code == 422


def test_orders_read_admin_limit_zero(admin_client):
    response = admin_client.get("/orders/?limit=0")
    assert response.status_code == 422


def test_orders_read_admin_limit_incorrect(admin_client):
    response = admin_client.get("/orders/?limit=incorrect")
    assert response.status_code == 422


def test_orders_read_admin_limit_too_large(admin_client):
    response = admin_client.get("/orders/?limit=10000")
    assert response.status_code == 422


def test_orders_read_admin_offset(admin_client):
    response = admin_client.get("/orders/?limit=100&offset=5")
    assert response.status_code == 200
    assert len(response.json()) != 1


def test_orders_read_admin_offset_negative(admin_client):
    response = admin_client.get("/orders/?limit=100&offset=-1")
    assert response.status_code == 422


def test_orders_read_admin_offset_zero(admin_client):
    response = admin_client.get("/orders/?limit=100&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_orders_read_admin_offset_incorrect(admin_client):
    response = admin_client.get("/orders/?limit=100&offset=incorrect")
    assert response.status_code == 422


def test_orders_read_admin_offset_too_large(admin_client):
    response = admin_client.get("/orders/?limit=100&offset=10000")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_orders_update_admin(admin_client):
    response = admin_client.patch("/orders/update/5", json={"administrator_id": 2})
    assert response.status_code == 200
    json = response.json()
    assert json == {
        'administrator': {
            'email': 'jadoe@example.com',
            'full_name': 'Jane Doe',
            'id': 2
        },
        'customer_car': {
            'car': {'brand_name': 'Ferrari', 'model': '488 GTB'},
            'customer': {'email': 'cust@example.com', 'full_name': 'Customer2 User', 'id': 6},
            'id': 2,
            'license_plate': 'B456BB',
            'year': 2020
        },
        'employee': {'email': 'jadoe@example.com', 'full_name': 'Jane Doe', 'id': 2},
        'end_date': json['end_date'],
        'id': 5,
        'services': [
            {
                'id': 1,
                'name': 'Oil change',
                'price': {'cents': 200000,
                          'formatted': '2000 руб. 0 коп.',
                          'rubles': 2000},
                'time': {'minutes': 30, 'seconds': 1800}
            },
            {
                'id': 2,
                'name': 'Tire replacement',
                'price': {'cents': 500000,
                          'formatted': '5000 руб. 0 коп.',
                          'rubles': 5000},
                'time': {'minutes': 60, 'seconds': 3600}
            },
            {
                'id': 3,
                'name': 'Wheel alignment',
                'price': {'cents': 300000,
                          'formatted': '3000 руб. 0 коп.',
                          'rubles': 3000},
                'time': {'minutes': 40, 'seconds': 2400}
            }
        ],
        'start_date': json['start_date'],
        'status': 1,
        'total_price': 10000,
        'total_time': 130
    }


def test_orders_update_admin_incorrect_id(admin_client):
    response = admin_client.patch("/orders/update/incorrect", json={"name": "Test2"})
    assert response.status_code == 422


def test_orders_update_admin_not_found_id(admin_client):
    response = admin_client.patch("/orders/update/1000", json={"name": "Test2"})
    assert response.status_code == 404


def test_orders_delete_admin(admin_client):
    response = admin_client.delete("/orders/delete/3")
    assert response.status_code == 200


def test_orders_delete_admin_incorrect_id(admin_client):
    response = admin_client.delete("/orders/delete/incorrect")
    assert response.status_code == 422


def test_orders_delete_admin_not_found_id(admin_client):
    response = admin_client.delete("/orders/delete/1000")
    assert response.status_code == 404


def test_orders_delete_admin_deleted_id(admin_client):
    response = admin_client.delete("/orders/delete/3")
    assert response.status_code == 404
