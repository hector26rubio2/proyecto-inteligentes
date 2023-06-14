from enum import Enum

class OverUnderfittingOptions(str, Enum):
  crossValidation = "crossValidation"
  holdOut = "holdOut"
