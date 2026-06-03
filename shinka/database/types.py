# shinka/database/types.py
from enum import Enum

class AlgorithmCategory(Enum):
    DIVIDE_AND_CONQUER = "Divide and conquer"
    DYNAMIC_PROGRAMMING = "Dynamic programming"
    GREEDY = "Greedy"
    FREE = "Any/free"
