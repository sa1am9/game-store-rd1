from flask import abort, current_app


class AuthChecker:

    def __init__(self, db):
        self._db = db

    def check(self, resource, action, user_id):

        user = current_app.db['users'].user_id.fetchone(lambda x: x == user_id)
        if not user:
            abort(403)

        user_role = current_app.db['user_roles'].username.fetchone(lambda x: x == user['username'])

        if not user_role:
            abort(403)

        roles_permissions = current_app.db['roles_permissions'].role.query(lambda x: x == user_role['role'])

        for roles_permission in roles_permissions:
            perm_id = int(roles_permission['permission'])
            permission = current_app.db['permissions'].permission_id.fetchone(lambda x: x == perm_id)


            if permission['resource'] != resource:
                continue

            amount_of_actions = permission['actions']
            if action in amount_of_actions:

                return True

        abort(403)



