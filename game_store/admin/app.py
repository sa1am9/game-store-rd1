from flask import Flask

from game_store.admin.db import create_db
from game_store.admin.handlers import register_handlers as reg_admin_handlers


def create_app(name):

    app = Flask(name)

    if name.lower().startswith('test'):
        app.config['TESTING'] = True

    app.db = create_db()
    reg_admin_handlers(app)
    return app


def main():
    create_app('Game-Store').run(debug=True)


if __name__ == '__main__':
    main()
