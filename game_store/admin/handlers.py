from flask_restful import Resource, Api, reqparse
from flask import current_app, request
from .models import Users

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

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        params = parser.parse_args()
        ai_quotes = current_app.db['users'].storage
        for quote in ai_quotes:
            if (id == quote["id"]):
                quote["author"] = params["author"]
                quote["quote"] = params["quote"]
                return quote, 200



def register_handlers(app):

    api = Api(app)
    api.add_resource(UserHandler, '/user/<int:user_id>')
    api.add_resource(UserListHandler, '/users/')


    return api
