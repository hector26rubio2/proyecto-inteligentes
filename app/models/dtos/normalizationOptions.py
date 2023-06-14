from enum import Enum

class NormalizationOptions(str, Enum):
  minMax = "minMax"
  standarScaler = "standardScaler"