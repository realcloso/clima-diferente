from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "clima_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
clima_collection = db["clima"]
