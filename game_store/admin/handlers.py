from flask_restful import Resource, Api
<<<<<<< HEAD
from flask import current_app, request, jsonify
=======
from flask import current_app, request, g

from ..auth import auth
>>>>>>> 84e5bca94b88934d03019ec720ed04e965eff8f2


class UserHandler(Resource):

<<<<<<< HEAD
    def delete(self, user_id):
        try:
            user = current_app.db['users'].get_by_id(user_id)
            user['active'] = False
        except KeyError:
            return '', 404


    def get(self, user_id):
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if user['active']:
                return user
            else:
                return '', 404
        except:
            return '', 404

    def put(self, user_id):
        try:
            new_user_data = request.get_json()
            user = current_app.db['users'].get_by_id(user_id)
            if user['active']:
                for i in new_user_data.keys():
                    user[i] = new_user_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404


=======
    @auth.login_required
    def get(self, user_id):

        current_app.auth_checker.check('Users', 'read', g.user['user_id'])
        return current_app.db['users'].get_by_id(user_id)
>>>>>>> 84e5bca94b88934d03019ec720ed04e965eff8f2


class UserListHandler(Resource):

    @auth.login_required
    def get(self):
        try:
            return current_app.db['users'].storage
        except:
            return '', 404

    @auth.login_required
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['active'] = True
        current_app.db['users'].insert(data)


        
class UserSearchHandler(Resource):

    def get(self, field, value):
        users_list = list()
        all_users = current_app.db['users'].storage
        for id, fields in all_users.items():
            if fields['active'] and fields[field]==value:
                users_list.append(fields)
        return jsonify(users_list)


def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserSearchHandler, '/search/<field>/<value>')

    return api
