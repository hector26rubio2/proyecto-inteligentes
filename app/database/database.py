import pymongo
from app.config.database import ConfigDatabase
from app.models.models.modelEnty import ModelEnty

class DataBase:
  def __init__(self) :
    self._db = ConfigDatabase() 

  
  def insertCollection(self, document, collectionName):
    try: 
        collection =  self._db.getDB().get_collection(collectionName)
        collection.delete_many({})
        collection.insert_many(document)
    except pymongo.errors.WriteError as error:
        print("Error de escritura en mongo")
        raise error
    except Exception as error:
        raise error
  
  def getColeccion(self,dataset):
    if dataset in self._db.getDB().list_collection_names():
      return self._db.getDB().get_collection(dataset).find()
    else:
      return None
    
  def insertModel(self, model:ModelEnty) :
    models =  self._db.getBDModels()   
    models.insert_one(model.toDict())
    
  def top3Models(self):
    models =  self._db.getBDModels()
    
    data =models.aggregate([
        {"$sort": {"accuracy": -1, "precision": -1, "f1": -1}},
        {"$limit": 3}
    ])
    #data = models.find().sort([("accuracy", -1), ("precision", -1), ("f1", -1)]).limit(3)
    return list(data)  