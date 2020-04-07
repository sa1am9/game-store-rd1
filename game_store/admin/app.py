from flask import Flask

from .db import create_db
from .handlers import register_handlers as reg_admin_handlers
from ..auth.handlers import register_handlers as reg_auth_handlers


def create_app(name):

    app = Flask(name)

    if name.lower().startswith('test'):
        app.config['TESTING'] = True

    app.db = create_db()

    reg_admin_handlers(app)
    reg_auth_handlers(app)

    return app


def main():
    create_app('Game-Store').run(debug=True)


if __name__ == '__main__':
    main()
