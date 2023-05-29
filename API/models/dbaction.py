from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

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

# insert data of new users in database
def insertUser(data):
    client = connect()
    mydb = client["iot_database"]
    mycol = mydb["User"]

    mycol.insert_one(data)

def findUser(userEmail, numero):
    client = connect()
    mydb = client["iot_database"]
    mycol = mydb["User"]

    myQuery = {
        "email" : userEmail,
        "numero" : numero
        }
    
    x = mycol.find_one(myQuery)
    if x:
        return True
    else:
        return False
    