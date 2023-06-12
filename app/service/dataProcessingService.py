from datetime import datetime
import pandas as pd
import json
import os
from app.database.database import DataBase

class DataProcessingService :
  
  def __init__(self) :
    self.dataFrame = None
    self._dataBase = DataBase()
    
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
      filePath = os.path.join('./app/documents/', fileName)
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
