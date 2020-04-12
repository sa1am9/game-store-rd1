from pytest import fixture
from game_store.admin.app import create_app
from game_store.auth.token import encode_auth_token
from game_store.admin.models import Users


@fixture()
def user_data():
    return [{
        'name': 'Taras',
        'surname': 'Shevchenko',
        'email': 'taras@shevchenko.name',
        'password': 'Zapovit2.0'
    }, {
        'name': 'Ivan',
        'surname': 'Franko',
        'email': 'ivan@franko.name',
        'password': 'Kamenyar123'
    }, {
        'name': 'Lesya',
        'surname': 'Ukrainka',
        'email': 'lesya@ukrainka.name',
        'password': 'Mavka789'
    }]

@fixture()
def users_db(user_data):

    users = Users()
    for u in user_data:
        users.insert(u)
    return users


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


@fixture(scope='function')
def client(app_config):

    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!'})
        yield c


@fixture(scope='function')
def data():
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua", 'active': True, 'user_id': 1}
    user2 = {'name': "Vasy", 'surname': "Goloborodko", 'email': "vov@gov.ua", 'active': True, 'user_id': 2}
    yield {'user1': user1, 'user2': user2, }
