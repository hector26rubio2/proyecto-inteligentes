
from fastapi import APIRouter ,Response, status
from typing import Union,List
from fastapi import UploadFile

from app.models.dtos.graphicalAnalysis import GraphicalAnalysis
from ..models.dtos.nameDatase import NameDatase
from ..models.excepts.error import Error
from ..service.dataProcessingService import DataProcessingService


router = APIRouter(
    prefix="/dataProcessing",
    tags=["dataProcessing"]
)
dataProcessingService= DataProcessingService()
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}






@router.post("/loadFile",
            status_code=200,
            response_model= Union[NameDatase, Error])
async def fileUpload(file :UploadFile, response: Response):
  try:
    extension = file.filename.split('.')[1]
    if extension not in ALLOWED_EXTENSIONS:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return Error(message= "expect a file with .xlsx or csv extension.")
    return NameDatase(dataset= await dataProcessingService.saveFile(file,extension))

  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR



@router.post("/descriptFile",
            status_code=200,
            response_model = Union[dict, Error])
async def descriptFile(dataset :str, response: Response):
  try:
    statusFile,msg = dataProcessingService.describeDataset(dataset)
    if not statusFile :
      response.status_code = status.HTTP_404_NOT_FOUND
      return Error(message=msg )
    return msg

  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get("/datasets",
            status_code=200,
            response_model = Union[List[str], Error])
async def getDatasets( response: Response):
  try:
    return dataProcessingService.getDataset()


  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    Error(message=error )


@router.get("/dataTreatment/{dataset}",status_code=200,response_model= Union[NameDatase, Error])
async def dataTreatment(dataset: str, response: Response):
  try:
    dataFrame = dataProcessingService.searchFile(dataset)
    if not dataFrame:
      response.status_code = status.HTTP_404_NOT_FOUND
      return Error(message=  f"Dataset not found '{dataset}'" )
    resp = dataProcessingService.processMissingData(dataset)
    return NameDatase(dataset=resp)
  
  except Exception as error:
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get("/graphical/{dataset}",
            status_code=200,
            response_model= Union[GraphicalAnalysis, Error] )
async def graphicalStatistical(dataset: str,response: Response):
  try:
    codeStatus,msg, histogramsPath,matrixPath = dataProcessingService.graphicalAnalysis(dataset)
    if codeStatus != 200 :
      response.status_code = codeStatus
      return Error(message= msg)
    return GraphicalAnalysis(histogramsPath= histogramsPath,matrixPath= matrixPath)
  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR