from flask_restful import Resource, Api
from flask import current_app, request


class UserHandler(Resource):

    def get(self, user_id):
        return current_app.db['users'].get_by_id(user_id)


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
