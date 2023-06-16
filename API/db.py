import psycopg2
from psycopg2.extras import DictCursor
import click
from flask import current_app, g, flash

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
    exc = db.cursor()
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

def findPermission(token):
    db = get_db()
    exc = db.cursor(cursor_factory=DictCursor)
    exc.execute('SELECT * FROM "allow_to" WHERE token = %s', (token,))
    permission = exc.fetchone()

    return permission


"""Mongo DB database"""

from pymongo.mongo_client import MongoClient
import certifi
import pandas as pd

def connect():
    uri = "mongodb+srv://Hermann:5e9V25ZsSHXdeZl3@cluster0.zjliq0a.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    
    client = MongoClient(uri, tlsCAFile=certifi.where())
    
    return client

client = connect()

def insertDB(data):
    
    mydb = client["iot_database"]
    mycol = mydb["capteur"]

    mycol.insert_one(data)

def findData(token):
    client = connect()
    mydb = client["iot_database"]
    mycol = mydb["capteur"]

    myQuery = {
        'token' : token
    }

    result = []
    # find data without _id and sort them by created
    for x in mycol.find(myQuery ,{"_id":0, "token":0}).sort("created"): 
        result.append(x)
    return result

def findToken():
    db = get_db()
    exc = db.cursor(cursor_factory=DictCursor)
    exc.execute('SELECT username, token FROM "users"')
    results = exc.fetchall()
    tokens = pd.DataFrame(results).set_index(0)[1].to_dict()
    return tokens

# def highValue():
