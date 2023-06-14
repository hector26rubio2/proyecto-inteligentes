
from fastapi import APIRouter ,Response, status
from typing import  Union, List

from app.models.dtos.model import ModelTRES

from ..models.models.modelEnty import ModelEnty



from ..service.trainingService import TrainingService



from ..models.dtos.trainingModelDTO import TrainingModelDTO
from ..models.excepts.error import Error

router = APIRouter(
    prefix="/training",
    tags=["training"]
)
trainingService = TrainingService()


@router.get("/listModel",
            status_code= status.HTTP_200_OK,
            response_model= dict)

def listModels():
    """
    Este endpoint devuelve una lista de modelos disponibles.
    :return: Un diccionario que contiene la lista de modelos.
    """
    return trainingService.getModels()


@router.get("/top3Models",
            status_code= status.HTTP_200_OK,
            response_model= List[ModelTRES])
def top3Models():
    """
    Este endpoint devuelve los tres mejores modelos basados en las mejores métricas de accuracy, recall y F1-score.
    Los modelos son seleccionados en función de su desempeño en estas métricas.
    :return: Una lista de los tres mejores modelos.
    """
    return trainingService.getTop3Models()

@router.post("/trainingModel",
            status_code= status.HTTP_200_OK,
            response_model= Union[ ModelTRES, Error])
def trainingModel(trainingModel: TrainingModelDTO, response: Response):
    """
    Este endpoint se utiliza para entrenar un modelo utilizando los datos proporcionados.
    :param trainingModel: Un objeto que contiene los datos y la configuración del modelo de entrenamiento.
    :param response: La respuesta HTTP que se enviará al cliente.
    :return: Si el entrenamiento se realiza correctamente, devuelve los detalles del modelo entrenado.
             En caso contrario, devuelve un objeto de error con un mensaje descriptivo.
    """
    modelDict = trainingModel.dict()
    codeStatus,msg,dataFrame= trainingService.getDataFrame(trainingModel.dataset)
    if codeStatus != 200 :
        response.status_code = codeStatus
        return Error(message= msg)
    
    model =  ModelEnty(**modelDict ,dataframe =dataFrame)
    resp = trainingService.TrainingCase(model)
    if resp is None:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return Error( message="You have to verify that you have loaded the dataset or that the columns and target are correct.")
    return ModelTRES(**resp)
