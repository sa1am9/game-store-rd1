from flask import abort


class AuthChecker:

    def __init__(self, db):
        self._db = db

    def check(self, resource, action, user_id):

        try:
            for item in self._db['user-roles'].user.fetchall(lambda x: x == user_id):
                roles = item['name']

            for item in self._db['role-perms'].role.fetchall(lambda x: x in roles):
                permissions = item['perm']

            resource = self._db['resources'].name.fetchone(lambda x: x == resource)['resource_id']

            for permission in permissions:
                perm = self._db['perms'].get_by_id(permission)
                if perm['action'] == action and perm['resource'] == resource:
                    abort(200)

            abort(403)

        except TypeError:
            abort(403)

