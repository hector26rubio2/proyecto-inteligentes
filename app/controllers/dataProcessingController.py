
from fastapi import APIRouter ,Response, status
from typing import Union,List
from fastapi import UploadFile

from ..models.dtos.graphicalAnalysis import GraphicalAnalysis
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
  """
    Este endpoint permite cargar un archivo (formato .xlsx o .csv) y procesarlo.
    :param file: El archivo que se va a cargar.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Si el archivo se carga correctamente, devuelve los detalles del conjunto de datos procesado.
             En caso de error, devuelve un objeto de error con un mensaje descriptivo.
  """
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
  """
    Este endpoint permite obtener una descripción del conjunto de datos especificado.
    :param dataset: El nombre o identificador del conjunto de datos.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Si el conjunto de datos se encuentra, devuelve una descripción del mismo en formato de diccionario.
             En caso contrario, devuelve un objeto de error con un mensaje descriptivo.
  """
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
  """
    Este endpoint permite obtener la lista de conjuntos de datos disponibles.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Devuelve una lista de nombres de conjuntos de datos disponibles.
             En caso de error, devuelve un objeto de error con un mensaje descriptivo.
  """
  try:
    return dataProcessingService.getDataset()


  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    Error(message=error )


@router.get("/dataTreatment/{dataset}",status_code=200,response_model= Union[NameDatase, Error])
async def dataTreatment(dataset: str, response: Response):
  """
    Este endpoint permite realizar el tratamiento de datos para un conjunto de datos específico.
    :param dataset: El nombre o identificador del conjunto de datos.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Si el conjunto de datos se encuentra, devuelve los detalles del conjunto de datos procesado.
             En caso contrario, devuelve un objeto de error con un mensaje descriptivo.
  """
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
  """
    Este endpoint permite realizar un análisis gráfico y estadístico de un conjunto de datos específico.
    :param dataset: El nombre o identificador del conjunto de datos.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Si el análisis se realiza correctamente, devuelve los detalles del análisis gráfico y estadístico.
             En caso contrario, devuelve un objeto de error con un mensaje descriptivo.
  """
  try:
    codeStatus,msg, histogramsPath,matrixPath = dataProcessingService.graphicalAnalysis(dataset)
    if codeStatus != 200 :
      response.status_code = codeStatus
      return Error(message= msg)
    return GraphicalAnalysis(histogramsPath= histogramsPath,matrixPath= matrixPath)
  except Exception as error:
    print(error)
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR