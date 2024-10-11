from pymongo import MongoClient

MONGO_DETAILS = "mongodb://root:password@localhost:27017"; # config('MONGO_DATABASE')
client = MongoClient(MONGO_DETAILS)

database = client.myapi
