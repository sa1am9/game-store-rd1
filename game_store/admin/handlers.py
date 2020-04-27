from flask_restful import Resource, Api, abort

from flask import jsonify, current_app, request, g

from ..auth import auth


class UserHandler(Resource):

    @auth.login_required
    def delete(self, user_id):
        try:
            current_app.auth_checker.check('User', 'delete', g.user['user_id'])
            current_app.db['users'].hide(user_id)
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def get(self, user_id):
        try:
            current_app.auth_checker.check('User', 'read', g.user['user_id'])
            user = current_app.db['users'].get_by_id(user_id)
            return user if user is not None else ''
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def put(self, user_id):
        try:
            new_user_data = request.get_json()
            current_app.auth_checker.check('User', 'update', g.user['user_id'])

            user = current_app.db['users'].get_by_id(user_id)
            if user:
                for i in new_user_data.keys():
                    user[i] = new_user_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


class UserListHandler(Resource):

    @auth.login_required
    def get(self):
        try:
            current_app.auth_checker.check('UserList', 'list', g.user['user_id'])
            return current_app.db['users'].storage
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def post(self):
        current_app.auth_checker.check('UserList', 'add', g.user['user_id'])
        user_dict = request.get_json()
        data = user_dict['user']
        current_app.db['users'].insert(data)




class UserSearchHandler(Resource):

    @auth.login_required
    def get(self, field, value):

        searched_users = current_app.db['users'].search(field, value)
        return jsonify(list(searched_users))


class RoleListHandler(Resource):

    @auth.login_required
    def get(self):
        try:
            current_app.auth_checker.check('RoleList', 'list', g.user['user_id'])
            return current_app.db['roles'].storage
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def post(self):
        try:
            current_app.auth_checker.check('RoleList', 'add', g.user['user_id'])

            user_dict = request.get_json()
            data = user_dict['role']
            current_app.db['roles'].insert(data)
        except KeyError:
            return abort(500)


class RoleHandler(Resource):

    @auth.login_required
    def get(self, role_name):
        try:
            current_app.auth_checker.check('Role', 'read', g.role['user_id'])

            role = current_app.db['roles'].name.fetchone(lambda x: x == role_name)

            return role if role is not None else ''
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


    @auth.login_required
    def delete(self, role_name):
        try:
            current_app.auth_checker.check('Role', 'delete', g.user['user_id'])
            current_app.db['roles'].delete(role_name)
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


    @auth.login_required
    def put(self, role_name):
        try:
            current_app.auth_checker.check('Role', 'update', g.user['user_id'])
            new_role_data = request.get_json()
            role = current_app.db['roles'].name.fetchone(lambda x: x == role_name)
            if role:
                for i in new_role_data.keys():
                    role[i] = new_role_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


class UserRolesHandler(Resource):

    @auth.login_required
    def get(self, username):

        current_app.auth_checker.check('UserRoles', 'read', g.user['user_id'])
        user_role = current_app.db['user_roles'].username.fetchone(lambda x: x == username)
        if not user_role:
            return '', 404

        answer_data = {'username': username, 'roles': [{'name': user_role['role'], 'resources': []}]}

        roles_permissions = current_app.db['roles_permissions'].role.query(lambda x: x == user_role['role'])
        for roles_permission in roles_permissions:
            perm_id = int(roles_permission['permission'])
            permission = current_app.db['permissions'].permission_id.fetchone(lambda x: x == perm_id)
            answer_data['roles'][0]['resources'].append({'resource': permission['resource'],
                                                         'actions': permission['actions']})

        return answer_data


    @auth.login_required
    def put(self, username):
        current_app.auth_checker.check('UserRoles', 'update', g.user['user_id'])
        new_user_role_data = request.get_json()['user_role']
        user_role = current_app.db['user_roles'].username.fetchone(lambda x: x == username)
        if not user_role:
            return '', 404

        for i in new_user_role_data.keys():
            user_role[i]= new_user_role_data[i]
        return 200


class UserRolesListHandler(Resource):

    @auth.login_required
    def get(self):
        return current_app.db['user_roles'].storage



class PermissionListHandler(Resource):

    @auth.login_required
    def get(self):
        current_app.auth_checker.check('PermissionList', 'list', g.user['user_id'])
        return current_app.db['permissions'].storage


def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserSearchHandler, '/search/<field>/<value>')
    api.add_resource(PermissionListHandler, '/permissions/')

    api.add_resource(RoleHandler, '/role/<string:role_name>')
    api.add_resource(RoleListHandler, '/roles/')
    api.add_resource(UserRolesHandler, '/user_roles/<username>')
    api.add_resource(UserRolesListHandler, '/user_roles/')

    return api
