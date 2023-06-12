import pymongo
from app.config.database import ConfigDatabase

class DataBase:
  def __init__(self) :
    self._db = ConfigDatabase() 

  
  def insertCollection(self, document, collection_name):
    try: 
        collection =  self._db.getDB().get_collection(collection_name)
        beforeCount = collection.count_documents({})
        collection.insert_many(document)

        return collection.count_documents({}) - beforeCount
    
    except pymongo.errors.WriteError as error:
        print("Error de escritura en mongo")
        raise error
    except Exception as error:
        raise error
  