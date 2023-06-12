from pymongo import MongoClient
from app.config.settings import Config


client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DBNAME]