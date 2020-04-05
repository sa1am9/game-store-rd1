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
    assert client.get('/user/1').status_code == 404
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
    user0 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua",}
    client.post('/users/', json={'user': user0})
    client.delete('/user/0')

    assert client.delete('user/1').status_code == 404

    resp = client.get('/user/0')
    user0['active'] = False
    assert  resp.json == ''

def test_search_user(client):
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua", }
    client.post('/users/', json={'user': user1})
    user2 = {'name': "Vas", 'surname': "Goloborodko", 'email': "vov@gov.ua", }
    client.post('/users/', json={'user': user2})
    resp = client.get('search/surname/Goloborodko')
    user1['active'] = True
    user2['active'] = True
    users = [user1, user2]
    #users.append(user1)

    assert resp.json == users


