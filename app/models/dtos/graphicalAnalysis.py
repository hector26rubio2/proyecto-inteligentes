from pydantic import BaseModel

class GraphicalAnalysis(BaseModel):
    histogramsPath : str
    matrixPath : str
