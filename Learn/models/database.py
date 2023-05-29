from pymongo.mongo_client import MongoClient
import certifi

def connect():
    uri = "mongodb+srv://Hermann:5e9V25ZsSHXdeZl3@cluster0.zjliq0a.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile=certifi.where())

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print("impossible de se connecter")
    return client

# find data in mongo database
def findData():
    client = connect()
    mydb = client["iot_database"]
    mycol = mydb["capteur"]

    result = []
    # find data without _id and sort them by created
    for x in mycol.find({},{"_id":0, "temperature":1, "humidity":1, "created":1}).sort("created"): 
        result.append(x)
    return result
