def test_add_user(client, data, token_auth):
    """
    Test creating user, post to server and creating personal url.
    :param client:
    :param data:
    :param token_auth:
    :return:
    """
    user1 = data['user1']
    client.post('/users/', json={'user': user1})

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
    client.post('/users/', json={'user': user1})

    resp = client.get('/user/1', headers=token_auth)

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

    client.post('/users/', json={'user': user1})
    client.put('/user/1', json=user2, headers=token_auth)

    resp = client.get('/user/1', headers=token_auth)

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

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})

    resp = client.get('/users/', headers=token_auth)
    del resp.json['0']
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

    client.post('/users/', json={'user': user1})
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
    client.post('/users/', json={'user': user1})

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

    client.post('/users/', json={'user': user1})
    client.post('/users/', json={'user': user2})

    resp = client.get('search/surname/Goloborodko', headers=token_auth)

    users = [user1, user2]

    assert resp.json == users


