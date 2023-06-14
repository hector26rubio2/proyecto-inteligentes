from pydantic import BaseModel


class ModelTRES(BaseModel):
  modelType: str
  normalizationType: str
  overUnderfitting: str
  target: str
  allFeatures : bool 
  features: list[str]  = []
  accuracy: float 
  precision: float 
  recall: float 
  f1: float 
  modelName: str
  dataset: str