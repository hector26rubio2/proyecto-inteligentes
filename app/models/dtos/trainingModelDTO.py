
from pydantic import BaseModel
from .kernelOptions import KernelOptions

from .modelOptions import ModelOptions
from .normalizationOptions import NormalizationOptions
from .overUnderfittingOptions import OverUnderfittingOptions

class TrainingModelDTO(BaseModel):
  dataset :str
  modelType: ModelOptions 
  normalizationType: NormalizationOptions 
  overUnderfitting: OverUnderfittingOptions
  target: str 
  allFeatures : bool  = False
  features: list[str]  =  None
  percentTests: int 
  numberFolds: int 
  neighbors: int 
  kernel: KernelOptions  
  depth: int