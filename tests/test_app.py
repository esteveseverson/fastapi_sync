from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Olá Mundo'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testusername',
                'email': 'test@test.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'testusername2',
            'password': '123',
            'email': 'test@test.com',
        },
    )
    assert response.json() == {
        'id': 1,
        'username': 'testusername2',
        'email': 'test@test.com',
    }


def test_update_user_inexistente(client):
    response = client.put(
        '/users/2',
        json={
            'id': 2,
            'username': 'testusername3',
            'password': '123',
            'email': 'test@test.com',
        },
    )
    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_inexistente(client):
    response = client.delete(
        '/users/2',
    )
    assert response.json() == {'detail': 'USER NOT FOUND'}
