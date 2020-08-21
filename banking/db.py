import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext
import os


def get_db():

    if 'db' not in g:
        # @TODO: Move to config
        g.db = sqlite3.connect(os.path.join(
            current_app.instance_path, 'banking.sqlite3')
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """ If this request connected to the database, close the connection. """
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    """ Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    click.echo('Initialized the database.')


def init_app(app):
    """ Register database functions with the Flask app. This is called by the application factory. """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_cmd)