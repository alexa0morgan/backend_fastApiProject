def test_correct_auth(guest_client):
    response = guest_client.post(
        '/token',
        data={"username": "bbrown@example.net", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)


def test_auth_with_incorrect_password(guest_client):
    response = guest_client.post(
        '/token',
        data={"username": "bbrown@example.net", "password": "password2"}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_auth_with_incorrect_username(guest_client):
    response = guest_client.post(
        '/token',
        data={"username": "doesnotexist@at.all", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_auth_with_empty_data(guest_client):
    response = guest_client.post(
        '/token',
        data={"username": "", "password": ""}
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {'input': None, 'loc': ['body', 'username'], 'msg': 'Field required', 'type': 'missing'},
            {'input': None, 'loc': ['body', 'password'], 'msg': 'Field required', 'type': 'missing'}
        ]
    }


def test_auth_with_empty_password(guest_client):
    response = guest_client.post(
        '/token',
        data={"username": "jdoe@example.net", "password": ""}
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {'input': None, 'loc': ['body', 'password'], 'msg': 'Field required', 'type': 'missing'}
        ]
    }
