from flask import current_app, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from .token import encode_auth_token, decode_auth_token, InvalidToken, ExpiredToken


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
auth = MultiAuth(token_auth, basic_auth)


@auth.login_required
def get_auth_token():

    config = current_app.config
    user_email = g.user['email']
    t = encode_auth_token(user_email, config)
    return t.decode()


@basic_auth.verify_password
def verify_basic_auth(username_or_token, password):

    config = current_app.config
    user_data = username_or_token
    try:
        # first try to authenticate by token
        user_data = decode_auth_token(username_or_token, config)
    except ExpiredToken:
        return False
    except InvalidToken:
        pass

    # try to authenticate with username/password
    db_users = current_app.db['users']
    user = db_users.email.fetchone(lambda x: x == user_data)

    if not user or not verify_password(password, user['password']):
        return False

    g.user = user
    return True


@token_auth.verify_token
def verify_token_auth(token):

    config = current_app.config
    user_data = None
    try:
        user_data = decode_auth_token(token, config)
    except ExpiredToken:
        return False
    except InvalidToken:
        pass

    # try to authenticate with username/password
    db_users = current_app.db['users']
    user = db_users.email.fetchone(lambda x: x == user_data)

    if not user:
        return False

    g.user = user
    return True


def verify_password(client_password, user_password):

    return client_password == user_password
