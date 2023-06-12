from datetime import datetime
import pandas as pd
import json
import os
from app.database.database import DataBase

class DataProcessingService :
  DIRECTORY = './app/documents/'
  def __init__(self) :
    self.dataFrame = None
    self._dataBase = DataBase()
    
#carga data
  async def saveFile(self, file,extension):
    try:
      filePath,fileFullName = await self._saveFile(file)
      self._createDateFrame(extension,filePath)
      self._loadDataFrame(fileFullName)    
      
      return f"{fileFullName}"
    except Exception as error:
        raise error
      
  def _createDateFrame(self,extension,filePath) :
    if extension == 'xlsx' :
      self._createDataFrameExcel(filePath)
    else:
      self._createDataFrameCsv(filePath)
      
      
  async def _saveFile(self, file):
    try:
      
      fileContent = await file.read()
      fileName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.filename
      filePath = os.path.join( self.DIRECTORY, fileName)
      with open(filePath, "wb") as f:
        f.write(fileContent)
        
      return filePath,fileName.split('.')[0]
    except Exception as error:
      raise error

    
  def _createDataFrameExcel(self,path):
    try:
      self._setDataFrame(pd.read_excel(path))
    except Exception as error: 
      raise error
    
  def _createDataFrameCsv(self,path):
    try:
      self._setDataFrame(pd.read_csv(path, delimiter=","))
    except Exception as error: 
      raise error
    
  def _setDataFrame(self, dataFrame):
    self.dataFrame = dataFrame
    
    
  def _loadDataFrame(self,fileName):
    try:
      dataToInsert = self.dataFrame.to_json(orient='records')
      return self._dataBase.insertCollection(json.loads(dataToInsert),fileName)
    except Exception as error: 
      raise error
# hasta aqui


  def describeDataset(self,dataset):
    pathFile,extension = self._searchFile(dataset)
    if pathFile is None:
      return False, f'Dataset not found "{dataset}"'
    self._createDateFrame(extension,pathFile) 
    dict = self._describeDataset()
        
    return  True,dict
  
  
  def _searchFile(self, dataset):
    for root, _, files in os.walk(self.DIRECTORY):      
        if f"{dataset}.csv" in files:
            return f"{os.path.join(root, dataset)}.csv" ,'csv'
        if f"{dataset}.xlsx" in files:
            return f"{os.path.join(root, dataset)}.xlsx" ,'xlsx'
    return None,_

  def _describeDataset(self):
    try:
      return None if self.dataFrame is None else  self._describeData()
    except Exception as error:
      raise error

  def _describeData(self):
        try:
            firstRecordDict = self.dataFrame.iloc[0].to_dict()
            return {key: type(value).__name__ for key, value in firstRecordDict.items()}
        except Exception as error:
            raise error
          
          
  def getDataset(self):
    file_names = []
    for file_name in os.listdir(self.DIRECTORY):
        if os.path.isfile(os.path.join(self.DIRECTORY, file_name)):
            file_names.append(file_name)
    return file_names
    
