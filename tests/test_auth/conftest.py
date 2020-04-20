import os
from pytest import fixture
from game_store.admin.app import create_app


@fixture(scope='function')
def config():
    return {
        'JWT_TTL_SECONDS': 300,
        'JWT_SECRET_KEY': str(os.urandom(24))
    }


@fixture(scope='function')
def client(config):
    app = create_app('Test-Auth')
    app.config.from_mapping(config)
    with app.test_client() as c:
        c.application.db['users'].insert({'name': 'Root', 'email': 'root@example.com', 'password': 'Qwerty12344556'})
        yield c

