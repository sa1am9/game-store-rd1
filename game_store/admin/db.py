from .models import Users, Roles, Resources, UserRoles, Permissions, RolePermissions, Tokens


def create_db():

    return {
        'users': Users(),
        'roles': Roles(),
        'resources': Resources(),
        'user_roles': UserRoles(),
        'roles_permissions': RolePermissions(),
        'permissions': Permissions(),
        'tokens': Tokens()

    }
