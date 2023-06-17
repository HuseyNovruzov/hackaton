import pymongo
from pymongo import MongoClient
from config import settings

client = MongoClient(settings.DATABASE_URI,serverSelectionTimeoutMS=5000)

# Create db and Collections

db = client[settings.MONGO_INITDB_DATABASE]

User = db.users
Report = db.reports

User.create_index([("email", pymongo.ASCENDING)], unique=True)