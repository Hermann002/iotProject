from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import pymongo
import pandas as pd

def connect():
    uri = "mongodb+srv://Hermann:5e9V25ZsSHXdeZl3@cluster0.zjliq0a.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile=certifi.where())

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    mydb = client["iot_database"]
    mycol = mydb["capteur"]

    result = []
    for x in mycol.find({}).sort("date"):
        result.append(x)
    return result