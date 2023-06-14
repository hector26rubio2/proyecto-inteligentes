from datetime import datetime
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import json
import os
from app.database.database import DataBase


class DataProcessingService :
  DIRECTORY = './app/documents/'
  HOST = "http://127.0.0.1:8000/"
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
      self._dataBase.insertCollection(json.loads(dataToInsert),fileName)
    except Exception as error: 
      raise error
# hasta aqui


  def searchFile(self,dataset):
    pathFile,extension = self._searchFile(dataset)
    if pathFile is None:
      return False
    self._createDateFrame(extension,pathFile) 
    return True
    

  def describeDataset(self,dataset):
    if self.searchFile(dataset):
      dict = self._describeDataset()
      return  True,dict
    else:
      return False, f"Dataset not found '{dataset}'" 
  
  
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
    fileNames = []
    for fileName in os.listdir(self.DIRECTORY):
        if os.path.isfile(os.path.join(self.DIRECTORY, fileName)):
            fileNames.append(fileName.split('.')[0])
    return fileNames
  
  def processMissingData(self,dataset):
    try:
      if self.dataFrame is None:
        return None
      fileFullName =f"{dataset}_limpio"
      self._missingDataDiscard()      
      self._missingDataImputation()      
      self._loadDataFrame(fileFullName)
      return fileFullName
    except Exception as error:
      raise error
    
  def _missingDataDiscard(self):
    try:
      dataFrameNN = self.dataFrame.dropna()  
      self._setDataFrame(dataFrameNN)     
    except Exception as error:
      print(error)
      raise error
    
  def _missingDataImputation(self):
      try:
          numColumns = self.dataFrame.select_dtypes(np.number).columns
          objColumns = self.dataFrame.select_dtypes(object).columns
          dataFrame = self._averageImputation(self.dataFrame, numColumns)
          dataFrame = self._modeImputation(dataFrame, objColumns)
          self._setDataFrame(dataFrame)
      except Exception as error:
          raise error
        
  def _averageImputation(self, dataFrame, numColumns):
    for column in numColumns:
      media = dataFrame[column].mean()
      dataFrame[column].fillna(media, inplace=True)
    return dataFrame

  def _modeImputation(self, dataFrame, objColumns):
    for column in objColumns:
      mode = dataFrame[column].mode()[0]
      dataFrame[column].fillna(mode, inplace=True)
    return dataFrame
  
  
  def graphicalAnalysis(self,dataset):
    if not self.searchDatase(dataset) :
      return 400, f"Dataset not found '{dataset}'","",""
    arr =  dataset.split('_')
    if arr[len(arr)-1] != "limpio":
      return 404, f"It is recommended to first do the treatment of missing data for the dataset '{dataset}'","",""
    histograms = self._histograms(dataset)
    correlationMatrix = self._correlationMatrix(dataset)
    
      
    return 200,"",histograms, correlationMatrix


  def _histograms(self,dataset):
    try:      
      dfNumeric = self.dataFrame.select_dtypes(np.number)
      plt.rcParams['figure.figsize'] = (19, 9)
      plt.style.use('ggplot')
      dfNumeric.hist()

      folderPath = self.createfolder("histograms")
      filePath = os.path.join(folderPath, dataset)
      plt.savefig(filePath)
      return f"{self.HOST}histograms/{dataset}.png"
    except Exception as error:
      print(f"error{error} hi")
      raise error

  def _correlationMatrix(self,dataset):
    try:
      dfNumeric =  self.dataFrame.select_dtypes(np.number)  
      correlationMatrix = dfNumeric.astype(float).corr()
      colorMap = plt.cm.coolwarm
      plt.figure(figsize=(12,12))
      plt.title('Correlation of Features', y=1.05, size=15)
      sb.heatmap(correlationMatrix,linewidths=0.1,vmax=1.0, square=True, cmap=colorMap,linecolor='white', annot=True)
      folderPath = self.createfolder("correlationMatrix")
      filePath = os.path.join(folderPath, dataset)
      plt.savefig(filePath)
      return f"{self.HOST}correlationMatrix/{dataset}.png"
    except Exception as error:
      print(f"error{error} ma")
      raise error
        
  def createfolder(self, folderName):
    folderPath = os.path.join(self.DIRECTORY, folderName)
    if not os.path.exists(folderPath):
      os.makedirs(folderPath)
    return folderPath
  
  
  def searchDatase(self,dataset):
    data =  self._dataBase.getColeccion(dataset)
    if data is None:
      return  False
    resultados = list(data)
    df = pd.DataFrame(resultados)
    self._setDataFrame(df)
    return True
    