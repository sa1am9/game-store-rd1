import os
from pytest import fixture
from game_store.admin.app import create_app

@fixture(scope='function')
def config():
    return {
        'JWT_TTL_SECONDS': 300,
        'JWT_SECRET_KEY': str(os.urandom(24))
    }


@fixture()
def app_config():

    return {
        'JWT_SECRET_KEY': '12345677890',
        'JWT_TTL_SECONDS': 300
    }


@fixture(scope='function')
def client(app_config):

    app = create_app('Test-Auth')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'name': 'Root', 'email': 'root@example.com', 'password': 'Qwerty12344556'})
        yield c

