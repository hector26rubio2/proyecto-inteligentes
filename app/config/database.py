from pymongo import MongoClient
from app.config.settings import Config

class ConfigDatabase:
  
  def __init__(self):
    self._client = MongoClient(Config.MONGO_URI)
    self.db =  self._client.get_database(Config.MONGO_DBNAME)

  def getDataset(self, datase):
    return self._client.get_database(datase)
  
  def getDB(self):
    return self.db