from pytest import fixture
from unittest import mock

from game_store.admin.app import create_app
from game_store.auth.token import encode_auth_token


@fixture()
def app_config():

    return {
        'JWT_SECRET_KEY': 'ASDFGHJKL:ZX',
        'JWT_TTL_SECONDS': 500
    }


@fixture(scope='function')
def client(app_config):

    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!'})
        yield c


@fixture(scope='function')
def data():
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua", }
    user2 = {'name': "Vasy", 'surname': "Goloborodko", 'email': "vov@gov.ua", }
    yield {'user1': user1, 'user2': user2, }


def test_add_user(client, data):
    """
    Test creating user, post to server and creating personal url.
    :param client:
    :param data:
    :return:
    """
    user1 = data['user1']
    client.post('/users/', json={'user': user1})
    assert client.get('/user/0').status_code == 200


def test_get_nonexistent_user(client, data):
    """
    Test creating user, post to server and try returning non-existent user.
    :param client:
    :param data:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1})
    assert client.get('/user/1').status_code == 404


def test_add_correct_user(client, data):
    """
    Test creating user, post to server and attempt returning correct user.
    :param client:
    :param data:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1})

    user1['active'] = True
    resp = client.get('/user/0')

    assert user1 == resp.json


def test_update_user(client, data):
    """
    Test creating user, post to server, update it with another user.
    :param client:
    :param data:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1})
    client.put('/user/0', json=user2)

    user2['active'] = True
    resp = client.get('/user/0')

    assert user2 == resp.json


def test_list_users(client, data):
    """
    Test creating 2 users, post to server and return both.
    :param client:
    :param data:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})

    user1['active'] = True
    user2['active'] = True

    resp = client.get('/users/')

    assert resp.json == {'0': user1, '1': user2}


def test_hide_user(client, data):
    """
    Test creating user, post to server and hide him(without deleting from db).
    :param client:
    :param data:
    :return:
    """
    user1 = data['user1']

    client.post('/users/', json={'user': user1})
    client.delete('/user/0')

    resp = client.get('/user/0')
    user1['active'] = False

    assert resp.json == ''


def test_hide_nonexistent_user(client, data):
    """
    Test creating user, post to server and deleting non-existent user.
    :param client:
    :param data:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1})

    assert client.delete('/user/1').status_code == 404


def test_search_user(client, data):
    """
    Test creating users, post to server and search by last name.
    :param client:
    :param data:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})

    resp = client.get('search/surname/Goloborodko')

    user1['active'] = True
    user2['active'] = True
    users = [user1, user2]

    assert resp.json == users



@fixture()
def token_auth(app_config):

    username = 'admin@gov.ua'
    token = encode_auth_token(username, app_config)
    return {
        'Authorization': b'Bearer ' + token
    }


def test_add_user(client, token_auth):

    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}

    client.post('/users/', json={'user': user1}, headers=token_auth)
    resp = client.get('/user/1', headers=token_auth)

    expected = user1.copy()
    expected.update({'user_id': mock.ANY})

    status_code = resp.status_code
    assert status_code == 200 and resp.json == expected

