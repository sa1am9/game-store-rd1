from .models import Users


def create_db():

    return {
        'users': Users()
    }
