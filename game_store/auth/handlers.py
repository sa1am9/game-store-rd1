from flask import Blueprint
from flask_restful import Api, Resource, abort

from . import get_auth_token


class LoginHandler(Resource):

    def post(self):
        try:
            return {'token': get_auth_token()}
        except Exception:
            abort(404)


def register_handlers(app):

    bp = Blueprint('auth', 'AUTHENTICATION')
    api = Api(bp)
    api.add_resource(LoginHandler, '/login')

    app.register_blueprint(bp)

    return api
