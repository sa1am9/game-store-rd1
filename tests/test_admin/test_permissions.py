from pytest import fixture
from game_store.admin.app import create_app

@fixture(scope='function')
def client(app_config, data, token_auth):
    app = create_app('Test-Game-Store')
    app.config.from_mapping(app_config)
    with app.test_client() as c:
        c.application.db['users'].insert({'email': "admin@gov.ua", 'password': 'S3cPa55w0rd!', 'username': 'sa1am9'})
        c.application.db['permissions'].insert(data['permission1'])
        c.application.db['permissions'].insert(data['permission2'])
        c.application.db['roles_permissions'].insert(data['roles_permission1'])
        c.application.db['roles'].insert(data['role1'])
        c.application.db['user_roles'].insert(data['user_role1'])
        c.application.db['tokens'].insert({'token': token_auth['Authorization'].decode().split()[1]})

        yield c



@fixture(scope='function', name='data')
def data():

    permission1 = {'name': 'Manager', 'resource': 'PermissionList',
                   'actions': ['list', 'read', 'add', 'update', 'delete']}
    permission2 = {'name': 'Manager', 'resource': 'comments', 'actions': ['list', 'read', 'add', 'update', 'delete']}

    roles_permission1 = {'role': 'Manager', 'permission': 0}
    role1 = {'name': 'Manager'}
    user_role1 = {'username': 'sa1am9', 'role': 'Manager'}

    return {'permission1': permission1, 'permission2': permission2, 'roles_permission1': roles_permission1,
            'role1': role1, 'user_role1': user_role1}


def test_permissions_list(client, token_auth, data):

    resp = client.get('/permissions/', headers=token_auth)
    assert resp.json == {'0': data['permission1'], '1': data['permission2']}
