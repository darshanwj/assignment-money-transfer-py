import sqlite3
import click
from flask import g
from flask.cli import with_appcontext
from . import app
import os


def get_db():

    if 'db' not in g:
        g.db = sqlite3.connect(app.config['_DATABASE'])
        g.db.row_factory = sqlite3.Row
        # g.db.set_trace_callback(print)

    return g.db


@app.teardown_appcontext
def close_db(e=None):
    """ If this request connected to the database, close the connection. """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """ Clear existing data and create new tables."""
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    init_db()
    click.echo('Initialized the database.')
