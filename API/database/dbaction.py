from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import pymongo

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