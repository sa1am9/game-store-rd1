from flask_restful import Resource, Api
from flask import current_app, request


class UserHandler(Resource):

    def delete(self, user_id):
        user = current_app.db['users'].get_by_id(user_id)
        try:
            user['active'] = False
        except KeyError:
            return '', 404


    def get(self, user_id):
        user = current_app.db['users'].get_by_id(user_id)
        if user['active']:
            return user
        else:
            return '', 404

    def put(self, user_id):
        new_user_data = request.get_json()
        try:
            user = current_app.db['users'].get_by_id(user_id)
            if user['active']:
                for i in new_user_data.keys():
                    user[i] = new_user_data[i]
            else:
                return '', 404
        except KeyError:
            return '', 404




class UserListHandler(Resource):

    def get(self):
        return current_app.db['users'].storage

    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        data['active'] = True
        current_app.db['users'].insert(data)

    def search(self):
        pass
        



def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')

    return api
