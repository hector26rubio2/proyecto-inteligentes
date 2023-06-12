from fastapi import APIRouter ,Response, status
from typing import Union,List

from fastapi import UploadFile

from ..models.dtos.nameDatase import NameDatase

from ..models.dtos.upLoadFile import UploadFileM
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
            response_model= Union[UploadFileM, Error])
async def fileUpload(file :UploadFile, response: Response):
  try:
    extension = file.filename.split('.')[1]
    if extension not in ALLOWED_EXTENSIONS:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return Error(message= "expect a file with .xlsx or csv extension.")
    return UploadFileM(dataset= await dataProcessingService.saveFile(file,extension))
    
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
    Error(message=error )
    

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
  
