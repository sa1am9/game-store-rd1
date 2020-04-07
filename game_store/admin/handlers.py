from flask_restful import Resource, Api
from flask import current_app, request, g

from ..auth import auth


class UserHandler(Resource):

    @auth.login_required
    def get(self, user_id):

        # current_app.auth_checker.check('Users', 'read', g.user['user_id'])
        return current_app.db['users'].get_by_id(user_id)


class UserListHandler(Resource):

    @auth.login_required
    def get(self):
        return current_app.db['users'].storage

    @auth.login_required
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        current_app.db['users'].insert(data)


def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')

    return api
