import mysql.connector
import click
from API.database import db_check
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    #g is the current request, so reuse a sql-connection in one request
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host='localhost',
            database='pims',
            user='pimsuser',
            passwd='pimspassword',
            charset='utf8',
            auth_plugin='mysql_native_password'
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    print('init-db')
    checker = db_check.DBChecker(get_db())
    checker.init()

def init_db_OLD():
    try:
        db = get_db()
        with current_app.open_resource('schema.sql') as f:
            cursor = db.cursor()
            cursor.execute(f.read().decode('utf-8'))
    except mysql.connector.errors.ProgrammingError:
        print('MySQL-Error: Table Structure already exists')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create the database"""
    init_db()
    click.echo('Initalized database')