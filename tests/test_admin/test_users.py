from pytest import fixture

from game_store.admin.app import create_app


@fixture(scope='function')
def client():

    app = create_app('Test-Game-Store')
    with app.test_client() as c:
        yield c


def test_add_user(client):

    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua"}
    client.post('/users/', json={'user': user1})
    resp = client.get('/user/0')

    assert user1 == resp.json
