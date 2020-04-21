from flask import Blueprint, request, current_app, g
from flask_restful import Api, Resource, abort

from . import get_auth_token, auth, encode_auth_token


class LoginHandler(Resource):

    def post(self):
        try:
            return {'token': get_auth_token()}
        except Exception:
            abort(404)

class LogoutHandler(Resource):
    @auth.login_required
    def post(self):
        config = current_app.config
        token = encode_auth_token(g.user['email'], config, True).decode()
        return {'token': token}



class UserRegisterHandler(Resource):
    def post(self):
        user_dict = request.get_json()
        data = user_dict['user']
        if current_app.db['users'].email.fetchone(lambda x: x == data['email']):
            return "Yje takoi email est, poka", 409
        current_app.db['users'].insert(data)
        return '', 200


def register_handlers(app):

    bp = Blueprint('auth', 'AUTHENTICATION')
    api = Api(bp)
    api.add_resource(LoginHandler, '/login')
    api.add_resource(UserRegisterHandler, '/register')
    api.add_resource(LogoutHandler, '/logout')

    app.register_blueprint(bp)

    return api
