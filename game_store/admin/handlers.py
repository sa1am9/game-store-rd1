from flask_restful import Resource, Api

from flask import jsonify, current_app, request, g

from ..auth import auth


class UserHandler(Resource):

    @auth.login_required
    def delete(self, user_id):
        try:
            current_app.db['users'].hide(user_id)
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def get(self, user_id):
        try:
            # current_app.auth_checker.check('Users', 'read', g.user['user_id'])
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
            return current_app.db['users'].storage
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    def post(self):
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
            return current_app.db['roles'].storage
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


    def post(self):
        user_dict = request.get_json()
        data = user_dict['role']
        current_app.db['roles'].insert(data)


class RoleHandler(Resource):

    @auth.login_required
    def get(self, role_id):
        try:
            # current_app.auth_checker.check('Roles', 'read', g.role['role_id'])
            role = current_app.db['roles'].get_by_id(role_id)
            return role if role is not None else ''
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


    @auth.login_required
    def delete(self, role_id):
        try:
            current_app.db['roles'].delete(role_id)
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


    @auth.login_required
    def put(self, role_id):
        try:
            new_role_data = request.get_json()
            role = current_app.db['roles'].get_by_id(role_id)
            if role:
                for i in new_role_data.keys():
                    role[i] = new_role_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


class ResourceListHandler(Resource):

    @auth.login_required
    def get(self):
        try:
            return current_app.db['resource'].storage
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    def post(self):
        user_dict = request.get_json()
        data = user_dict['resources']
        current_app.db['resources'].insert(data)


class ResourceHandler(Resource):

    @auth.login_required
    def get(self, role_id):
        try:
            # current_app.auth_checker.check('Roles', 'read', g.role['role_id'])
            role = current_app.db['resource'].get_by_id(role_id)
            return role if role is not None else ''
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def delete(self, role_id):
        try:
            current_app.db['resource'].delete(role_id)
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def put(self, resource_id):
        try:
            new_resource_data = request.get_json()
            role = current_app.db['resource'].get_by_id(resource_id)
            if role:
                for i in new_resource_data.keys():
                    role[i] = new_resource_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404
        except Exception:
            return '', 404


def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserSearchHandler, '/search/<field>/<value>')

    api.add_resource(RoleHandler, '/role/<string:role_name>')
    api.add_resource(RoleListHandler, '/roles/')
    api.add_resource(ResourceHandler, '/resource/<string:resource_name>')
    api.add_resource(ResourceListHandler, '/resources/')

    return api
