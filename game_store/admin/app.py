import argparse
import yaml
import typing

from flask import Flask



from game_store.admin.db import create_db
from game_store.admin.handlers import register_handlers as reg_admin_handlers
from game_store.auth.handlers import register_handlers as reg_auth_handlers
from game_store.auth.permission import AuthChecker



def create_app(name, config=None):

    app = Flask(name)
    if isinstance(config, typing.Mapping):
        try:
            validate_config(config)
        except ValueError:
            pass
        else:
            app.config.from_mapping(config)

    if name.lower().startswith('test'):
        app.config['TESTING'] = True

    app.db = create_db()
    app.auth_checker = AuthChecker(app.db)

    reg_admin_handlers(app)
    reg_auth_handlers(app)

    return app


def register_superuser_account(db):

    pass


def read_yaml_config(config_fo):

    if config_fo is None:
        return
    with config_fo:
        return yaml.safe_load(config_fo)


def validate_config(config):

    keys = ['JWT_SECRET_KEY']
    missing = []
    for key in keys:
        if key not in config:
            missing.append(key)
    if len(missing) > 0:
        raise ValueError(f"config missing keys: {', '.join(missing)}")


def arg_parse(app_name, args=None):

    parser = argparse.ArgumentParser(app_name)
    parser.add_argument('--config', type=argparse.FileType(), default=None)

    return parser.parse_args(args)


def main(app_name='Game-Store'):

    args = arg_parse(app_name)
    config = read_yaml_config(args.config)
    app = create_app(app_name, config=config)

    register_superuser_account(app.db)

    app.run(debug=True)


if __name__ == '__main__':
    main()

