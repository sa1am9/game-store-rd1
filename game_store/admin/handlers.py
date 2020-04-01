from flask_restful import Resource, Api
from flask import current_app, request


class UserHandler(Resource):

    def get(self, user_id):
        return current_app.db['users'].get_by_id(user_id)

    def put(self, user_id):
        new_user_data = request.get_json()
        try:
            user = current_app.db['users'].get_by_id(user_id)
            for i in new_user_data.keys():
                user[i] = new_user_data[i]
        except KeyError:
            return '', 404





class UserListHandler(Resource):

    def get(self):
        return current_app.db['users'].storage

    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        current_app.db['users'].insert(data)



def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')


    return api
