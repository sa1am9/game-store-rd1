from flask import abort


class AuthChecker:

    def __init__(self, db):
        self._db = db

    def check(self, resource, action, user_id):

        abort(403)
