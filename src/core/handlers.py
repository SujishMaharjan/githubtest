import inspect
from typing import Callable


class CommandHandlers:
    def __init__(self, name:str):
        self._name = name
        self._handlers = {}

    def handler(self, handler_func: Callable):
        #logger registering handler_func_name
        params = inspect.signature(handler_func).parameters
        self._handlers[params["cmd"]] = handler_func
        return handler_func
