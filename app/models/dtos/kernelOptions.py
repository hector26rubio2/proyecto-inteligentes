from enum import Enum

class KernelOptions(str, Enum):
  rbf = "rbf"
  poly = "poly"