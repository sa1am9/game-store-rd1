from pytest import fixture

from game_store.admin.app import create_app

@fixture(scope='function')
def client(app_config, token_auth):
    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'username': 'sa1am9'})
        c.application.db['permissions'].insert({'name': 'Manager', 'resource': 'User',
                                                'actions': ['list', 'read', 'add', 'update', 'delete', 'search']})
        c.application.db['permissions'].insert({'name': 'Manager', 'resource': 'UserList',
                                                'actions': ['list', 'read', 'add', 'update', 'delete', 'search']})
        c.application.db['permissions'].insert({'name': 'Manager', 'resource': 'UserSearch',
                                                'actions': ['list', 'read', 'add', 'update', 'delete', 'search']})
        c.application.db['roles_permissions'].insert({'role': 'Manager', 'permission': '0'})
        c.application.db['roles_permissions'].insert({'role': 'Manager', 'permission': '1'})
        c.application.db['roles_permissions'].insert({'role': 'Manager', 'permission': '2'})
        c.application.db['roles'].insert({'name': 'Manager'})
        c.application.db['user_roles'].insert({'username': 'sa1am9', 'role': 'Manager'})
        c.application.db['tokens'].insert({'token': token_auth['Authorization'].decode().split()[1]})

        yield c


@fixture(scope='function', name='data')
def data():
    user1 = {'name': "Vasyl", 'surname': "Goloborodko", 'email': "vova@gov.ua",
             'username': 'GoloVasya', 'password': 'ny8erbyv8edvq0e8dfv0yc8b0abq-cvb', 'active':True}


    user2 = {'name': "Illia", 'surname': "Saltykov", 'email': "kek@gmaail.com",
             'username': 'lol', 'password': '0000000000', 'active': True}

    return {'user1': user1, 'user2': user2,}



def test_add_user(client, data, token_auth):
    """
    Test creating user, post to server and creating personal url.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']
    client.post('/users/', json={'user': user1}, headers=token_auth)

    assert client.get('/user/1', headers=token_auth).status_code == 200


def test_get_nonexistent_user(client, data, token_auth):
    """
    Test creating user, post to server and try returning non-existent user.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1})

    assert client.get('/user/2', headers=token_auth).status_code == 404


def test_add_correct_user(client, data, token_auth):
    """
    Test creating user, post to server and attempt returning correct user.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1}, headers=token_auth)

    resp = client.get('/user/1', headers=token_auth)
    user1['user_id']=1
    assert user1 == resp.json


def test_update_user(client, data, token_auth):
    """
    Test creating user, post to server, update it with another user.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1}, headers=token_auth)
    client.put('/user/1', json=user2, headers=token_auth)

    resp = client.get('/user/1', headers=token_auth)
    user2['user_id'] = 1
    assert user2 == resp.json


def test_list_users(client, data, token_auth):
    """
    Test creating 2 users, post to server and return both.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1}, headers=token_auth)
    client.post('/users/', json={'user': user2}, headers=token_auth)

    resp = client.get('/users/', headers=token_auth)
    del resp.json['0']
    user1['user_id'] = 1
    user2['user_id'] = 2
    assert resp.json == {'1': user1, '2': user2}


def test_hide_user(client, data, token_auth):
    """
    Test creating user, post to server and hide him(without deleting from db).
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']

    client.post('/users/', json={'user': user1}, headers=token_auth)
    client.delete('/user/1', headers=token_auth)

    resp = client.get('/user/1', headers=token_auth)

    assert resp.json == ''


def test_hide_nonexistent_user(client, data, token_auth):
    """
    Test creating user, post to server and deleting non-existent user.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """

    user1 = data['user1']
    client.post('/users/', json={'user': user1}, headers=token_auth)

    assert client.delete('/user/2', headers=token_auth).status_code == 404


def test_search_user(client, data, token_auth):
    """
    Test creating users, post to server and search by last name.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']
    user2 = data['user2']

    client.post('/users/', json={'user': user1}, headers=token_auth)
    client.post('/users/', json={'user': user2}, headers=token_auth)

    resp = client.get('search/surname/Goloborodko', headers=token_auth)

    users = [user1,]
    user1['user_id'] = 1
    assert resp.json == users


