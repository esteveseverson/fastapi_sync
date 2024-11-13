from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# def test_read_user_by_id(client, user):
#    response = client.get('/users/1')
#
#    assert response.status_code == HTTPStatus.OK
#    assert response.json() == {
#       user.username: 'Teste',
#        user.email: 'test@test.com',
#        user.password: 'testtest',
#    }


# def test_read_user_inexistente(client):
#    response = client.get(
#        '/users/2',
#    )
#    assert response.status_code == HTTPStatus.NOT_FOUND
#    assert response.json() == {'detail': 'USER NOT FOUND'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': user.id,
            'username': 'testusername2',
            'password': '123',
            'email': 'test@test.com',
        },
    )
    assert response.json() == {
        'id': user.id,
        'username': 'testusername2',
        'email': 'test@test.com',
    }


# def test_update_user_inexistente(client):
#     response = client.put(
#         '/users/2',
#         json={
#             'id': 2,
#             'username': 'testusername3',
#             'password': '123',
#             'email': 'test@test.com',
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'USER NOT FOUND'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {'message': 'User deleted'}


# def test_delete_user_inexistente(client):
#     response = client.delete(
#         '/users/2',
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'USER NOT FOUND'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
