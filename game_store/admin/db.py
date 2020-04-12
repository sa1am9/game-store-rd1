from .models import Users, Roles, Resources


def create_db():

    return {
        'users': Users(),
        # 'roles': Roles(),
        # 'resources': Resources(),
    }
