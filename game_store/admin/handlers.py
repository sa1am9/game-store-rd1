from flask_restful import Resource, Api

from flask import jsonify, current_app, request

from ..auth import auth



class UserHandler(Resource):

    @auth.login_required
    def delete(self, user_id):
        try:
            user = current_app.db['users'].get_by_id(user_id)
            user['active'] = False
        except KeyError:
            return '', 404
        except Exception:
            return '', 404

    @auth.login_required
    def get(self, user_id):
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if user:
                return user
            else:
                return '', 404
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


    # @auth.login_required
    # def get(self, user_id):
    #     current_app.auth_checker.check('Users', 'read', g.user['user_id'])
    #     return current_app.db['users'].get_by_id(user_id)



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

    def get(self, field, value):
        users_list = list()
        all_users = current_app.db['users'].storage
        for id, fields in all_users.items():
            if fields['active'] and fields[field] == value:
                users_list.append(fields)
        return jsonify(users_list)


class RolesHandler(Resource):
    def get(self):
        pass

def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')
    api.add_resource(UserSearchHandler, '/search/<field>/<value>')

    return api
