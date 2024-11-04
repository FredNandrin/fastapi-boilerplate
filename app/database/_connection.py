from pymongo import MongoClient
from decouple import config

MONGO_DETAILS =  "mongodb://" +config('MONGODB_ADMINUSERNAME')+":"+config('MONGODB_ADMINPASSWORD')+"@"+ config('MONGO_DATABASE')+":"+config('MONGO_DATABASE_PORT') # "mongodb://root:password@localhost:27017"; 
client = MongoClient(MONGO_DETAILS)

database = client.myapi
