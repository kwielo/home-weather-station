import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_HOST='192.168.10.53',
        DB_PORT=5432,
        DB_USER='dev',
        DB_PASS='d3v',
        DB_NAME='weather_station',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def start():
        return 'hi'

    from . import db
    db.init_app(app)

    return app

