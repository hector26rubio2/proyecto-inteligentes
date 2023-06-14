
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
    return trainingService.getModels()


@router.get("/top3Models",
            status_code= status.HTTP_200_OK,
            response_model= List[ModelTRES])
def top3Models():
    return trainingService.getTop3Models()

@router.post("/trainingModel",
            status_code= status.HTTP_200_OK,
            response_model= Union[ ModelTRES, Error])
def trainingModel(trainingModel: TrainingModelDTO, response: Response):
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
