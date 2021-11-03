import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASS'],
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    # db init command here
