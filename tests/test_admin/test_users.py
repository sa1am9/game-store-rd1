from pytest import fixture

from game_store.admin.app import create_app


@fixture(scope='function')
def client():

    app = create_app('Test-Game-Store')
    with app.test_client() as c:
        yield c


def test_add_user(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua",}

    assert client.get('/users/').status_code == 200
    client.post('/users/', json={'user': user1})
    assert client.get('/user/0').status_code == 200
    user1['active']=True
    resp = client.get('/user/0')
    assert user1 == resp.json


def test_update_user(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua", }
    client.post('/users/', json={'user': user1})
    user2 = {'name': "Vasy", 'surname': "Golobo", 'email': "vov@gov.ua"}

    client.put('/user/0',json=user2)
    user2['active']=True
    resp = client.get('/user/0')
    assert user2 == resp.json


def test_list_users(client):

    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua",}
    user2 = {'name': "Vasy", 'surname': "Golobo", 'email': "vov@gov.ua",}


    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})
    user1['active'] = True
    user2['active'] = True
    resp = client.get('/users/')

    assert resp.json == {'0': user1, '1': user2}


def test_hide_user(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua",}
    client.post('/users/', json={'user': user1})
    client.delete('/user/0')
    resp = client.get('/user/0')
    user1['active'] = False
    assert  resp.json == ''




