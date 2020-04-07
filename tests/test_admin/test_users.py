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
