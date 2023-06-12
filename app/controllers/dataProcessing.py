from fastapi import APIRouter

from app.models.dtos.file import FileDTO


router = APIRouter(
    prefix="/dataProcessing",
    tags=["dataProcessing"]
)


@router.post("/loadFile")
def fileUpload(file :FileDTO):
  
    return {"mensaje": "Esta es la ruta 1"}
  
  
