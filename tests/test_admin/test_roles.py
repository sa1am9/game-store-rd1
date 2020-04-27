from unittest import mock
from game_store.admin.app import create_app
from pytest import fixture

@fixture(scope='function')
def client(app_config, token_auth):
    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'username': 'sa1am9'})
        c.application.db['permissions'].insert({'name': 'Manager', 'resource': 'Role',
                                                'actions': ['list', 'read', 'add', 'update', 'delete']})
        c.application.db['permissions'].insert({'name': 'Manager', 'resource': 'RoleList',
                                                'actions': ['list', 'read', 'add', 'update', 'delete']})
        c.application.db['roles_permissions'].insert({'role': 'Manager', 'permission': '0'})
        c.application.db['roles_permissions'].insert({'role': 'Manager', 'permission': '1'})
        c.application.db['roles'].insert({'name': 'Manager'})
        c.application.db['user_roles'].insert({'username': 'sa1am9', 'role': 'Manager'})
        c.application.db['tokens'].insert({'token': token_auth['Authorization'].decode().split()[1]})

        yield c


@fixture(scope='function', name='data')
def data():

    role1 = {'name': 'User'}
    role2 = {'name': 'Manager'}
    role3 = {'name': 'Admin'}

    get_role_manager = {'name': 'Manager', 'resources': [
        {'resource': 'Role', 'actions': ['list', 'read', 'add', 'update', 'delete']},
        {'resource': 'RoleList', 'actions': ['list', 'read', 'add', 'update', 'delete']},
    ]}

    return {'role1': role1, 'role2': role2, 'role3': role3, 'get_role_manager': get_role_manager}

def test_add_role(client, token_auth, data):
    role = data['role1']
    resp = client.post('/roles/', json={'role': role}, headers=token_auth)

    assert resp.status_code == 200


def test_add_role_wrong(client, token_auth, data):
    role = data['role1']
    role.update({'wrong_field': 'strange_data'})
    resp_wrong_request = client.post('/roles/', json={'wrong_request_field': role}, headers=token_auth)
    assert resp_wrong_request.status_code == 500


def test_get_role_from_db(client, token_auth, data):
    role = data['role2']
    get_role_manager = data['get_role_manager']
    client.post('/roles/', json={'role': role}, headers=token_auth)

    resp = client.get('/role/Manager', headers=token_auth)
    resp_wrong_role = client.get('/role/BadRole', headers=token_auth)

    assert resp.json == get_role_manager and resp_wrong_role.status_code == 404


def test_roles_list(client, token_auth, data):
    role1 = data['role1']
    role0 = data['role2']
    client.post('/roles/', json={'role': role1}, headers=token_auth)

    role1.update({'role_id': mock.ANY})
    role0.update({'role_id': mock.ANY})

    resp = client.get('/roles/', headers=token_auth)

    assert resp.json == {'0': role0, '1': role1}


def test_modify_role(client, token_auth, data):
    role = data['role1']
    role_modified = data['role3']
    wrong_role = {'wrong_field': 'wrong_data'}
    client.post('/roles/', json={'role': role}, headers=token_auth)

    resp = client.put(f'/role/{role["name"]}', json={'role': role_modified}, headers=token_auth)


    resp_wrong_field = client.put(f'/role/{role_modified["name"]}', json={'role': wrong_role}, headers=token_auth)

    resp_wrong_id = client.put('/role/42', json={'role': role_modified}, headers=token_auth)


    assert resp.status_code == 200  and resp_wrong_field.status_code == 404 \
        and resp_wrong_id.status_code == 404


def test_delete_role(client, token_auth, data):
    role = data['role1']
    client.post('/roles/', json={'role': role}, headers=token_auth)

    resp = client.delete('/role/1', headers=token_auth)
    resp_from_db = client.get('/role/1', headers=token_auth)
    resp_wrong_id = client.delete('/role/42', headers=token_auth)

    assert resp.status_code == 200 and resp_from_db.status_code == 404 and resp_wrong_id.status_code == 404
