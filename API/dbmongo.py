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
    for x in mycol.find(myQuery ,{"_id":0, "temperature":1, "humidity":1, "created":1}).sort("created"): 
        result.append(x)
    return result

def findToken():
    client = connect()
    mydb = client["iot_database"]
    mycol = mydb["capteur"]

    result = []
    tokens = [""]

    for x in mycol.find({},{"_id":0,"temperature":1, "humidity":1, "created":1, "token":1 }):
        result.append(x)
    results = pd.DataFrame(result)

    i = 0
    for x in results['token']:
        if x == tokens[i]:
            continue
        else:
            tokens.append(x)
        i = i + 1
    tokens.remove('')
    
    return tokens