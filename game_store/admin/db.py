from .models import Users, Roles, Resources, UserRoles, Permissions, RolePermissions


def create_db():

    return {
        'users': Users(),
        'roles': Roles(),
        'resources': Resources(),
        'user-roles': UserRoles(),
        'role-perms': RolePermissions(),
        'perms': Permissions(),

    }
