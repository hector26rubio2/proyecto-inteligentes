



import os
import pandas as pd
from app.database.database import DataBase
from app.models.dtos.model import ModelTRES
from app.models.models.modelEnty import ModelEnty


class TrainingService:
  
  PATH_MODELS="./app/models/trainModels/"
  
  def __init__(self):
    self.model =None
    self.repository = None
    self._dataBase = DataBase()

  def TrainingCase(self, model : ModelEnty):
    self.model = model
    features = self.model.getFeaturesAndTarget()
    if features is None:
      return None
      
    X, y = features
    X =  self.model.encoderCategoricalColumns(X)
    y = self.model.encoderTarget(y)        
    modelType = self.model.getModelType()
    model_trained = self._trainWithOutOverOrUnderfitting(modelType, X, y)
    self._dataBase.insertModel(self.model)

    return model_trained

  def getDataFrame(self,dataset):
    dataFrame = self._searchDatase(dataset) 
    if  dataFrame is None :
      return 400, f"Dataset not found '{dataset}'",None
    arr =  dataset.split('_')
    if arr[len(arr)-1] != "limpio":
      return 404, f"It is recommended to first do the treatment of missing data for the dataset '{dataset}'",None
    return 200, "",dataFrame
  
  def _searchDatase(self,dataset):
    data =  self._dataBase.getColeccion(dataset)
    return None  if data is None else  pd.DataFrame(list(data))
  
  
  
  def _trainWithOutOverOrUnderfitting(self, model, X, y):
    if self.model.overUnderfitting == "crossValidation":
      return self.model.crossValidation(model, self._normalization(X), y)
        
    if self.model.overUnderfitting == "holdOut":
      X_train, X_test, y_train, y_test = self.model.holdOut(X=X, y=y)
      return self.model.fitHoldOut(model=model,x_train=self._normalization(X_train),x_test=self._normalization(X_test),y_test= y_test,y_train=y_train)
    return None
  
  
  def _normalization(self, dataframe):
    if self.model.normalizationType == "minMax":
        return self.model.normalizationMinmax(dataframe)
    if self.model.normalizationType == "standardScaler":
        return self.model.normalizationStandarScaler(dataframe)
    
  def getModels(self):
    models = {}
    for dir in os.listdir(self.PATH_MODELS):
        dirFull = os.path.join(self.PATH_MODELS, dir)
        if os.path.isdir(dirFull):
            nameFiles = self.getNameFiles(dirFull)
            models[dir] = nameFiles
    return models
  
  def getNameFiles(self,dir):
    names = []
    for file in os.listdir(dir):
        name, extension = os.path.splitext(file)
        names.append(name)
    return names
  
  def getTop3Models(self):
    documents = self._dataBase.top3Models()
    modelosTres = []
    for document in documents:
        modeloTres = ModelTRES(**document)
        modelosTres.append(modeloTres)

    return modelosTres
    