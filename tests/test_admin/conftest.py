from pytest import fixture
from game_store.auth.token import encode_auth_token


@fixture()
def app_config():

    return {
        'JWT_SECRET_KEY': 'ASDFGHJKL:ZX',
        'JWT_TTL_SECONDS': 500
    }


@fixture()
def token_auth(app_config):

    username = 'admin@gov.ua'
    token = encode_auth_token(username, app_config)
    return {
        'Authorization': b'Bearer ' + token
    }




