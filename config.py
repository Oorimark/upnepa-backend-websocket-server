import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

""" SETTING UP DATABASE CONNECTION """

connection_string = f"mongodb+srv://{os.getenv('DB_CONNECTION_USERNAME')}:{os.getenv('DB_CONNECTION_PASSWORD')}@cluster0.xcz3g.mongodb.net/?retryWrites=true&w=majority"

try:
    cluster = MongoClient(connection_string)
except Exception as e:
    raise Exception('MongoClient is not connected to mongo url')
else:
    db = cluster['UPNEPA_DATA_HOUSE']
    parameterCollection = db['parameters']
