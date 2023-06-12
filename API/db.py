import psycopg2
from psycopg2.extras import DictCursor
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
        g.db = psycopg2.connect(
            host="digishop.postgres.database.azure.com",
            port=5432,
            dbname="iot_database",
            user="digipos",
            password="postgres12@", 
            )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    exc = db.cursor(cursor_factory=DictCursor)
    with current_app.open_resource('schema.sql') as f:
        exc.execute(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)