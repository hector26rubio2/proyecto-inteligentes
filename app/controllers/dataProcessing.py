from fastapi import APIRouter ,Response, status
from typing import Union

from fastapi import UploadFile
from app.models.dtos.upLoadFile import UploadFileM
from app.models.excepts.error import Error
from app.service.dataProcessingService import DataProcessingService


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
    
  
  
