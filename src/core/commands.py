import inspect
from typing import Callable
from returns.result import Result



class Command:
    def __init__(self):
        self._result = Result | None = None 
    


