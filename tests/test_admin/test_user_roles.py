from pytest import fixture
from game_store.admin.app import create_app


@fixture(scope='function', name='data')
def data(token_auth):

    user_role1 = {'username': 'sa1am9', 'role': 'Manager'}
    user_role2 = {'username': 'sa1am8', 'role': 'User'}

    permission1 = {'name': 'Manager', 'resource': 'UserRoles', 'actions': ['list', 'read', 'add', 'update', 'delete']}
    permission2 = {'name': 'Manager', 'resource': 'comments', 'actions': ['list', 'read', 'add', 'update', 'delete']}

    roles_permission1 = {'role': 'Manager', 'permission': 0}
    roles_permission2 = {'role': 'Manager', 'permission': 1}

    role1 = {'name': 'Manager'}
    role2 = {'name': 'User'}

    token = token_auth['Authorization'].decode()
    token = {'token': token.split()[1]}

    get_user_role_resp = {'roles': [{'name': 'Manager',
                                    'resources': [{'actions': ['list', 'read', 'add', 'update', 'delete'],
                                                   'resource': 'UserRoles'},
                                                  {'actions': ['list', 'read', 'add', 'update',  'delete'],
                                                   'resource': 'comments'}]}],
                          'username': 'sa1am9'}

    return {'user_role1': user_role1, 'user_role2': user_role2, 'permission1': permission1, 'permission2': permission2,
            'roles_permission1': roles_permission1, 'roles_permission2': roles_permission2,
            'role1': role1, 'role2': role2, 'get_user_role_resp': get_user_role_resp, 'token': token}


@fixture(scope='function')
def client(app_config, data):
    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'username': 'sa1am9'})
        c.application.db['permissions'].insert(data['permission1'])
        c.application.db['permissions'].insert(data['permission2'])
        c.application.db['user_roles'].insert(data['user_role1'])
        c.application.db['roles_permissions'].insert(data['roles_permission1'])
        c.application.db['roles_permissions'].insert(data['roles_permission2'])
        c.application.db['roles'].insert(data['role1'])
        c.application.db['roles'].insert(data['role2'])
        c.application.db['tokens'].insert(data['token'])

        yield c


def test_get_user_role_from_db(client, data, token_auth):

    resp = client.get('/user_roles/sa1am9', headers=token_auth)
    assert resp.json == data['get_user_role_resp']


def test_modify_user_role(client, data, token_auth):

    user_role_modify = data['user_role2']
    resp = client.put('/user_roles/sa1am9', json={'user_role': user_role_modify}, headers=token_auth)

    resp_from_db = client.get('/user_roles/', headers=token_auth)
    user_role_modify.update({'ur_id': 0})
    assert resp.status_code == 200 and resp_from_db.json == {'0': user_role_modify}
