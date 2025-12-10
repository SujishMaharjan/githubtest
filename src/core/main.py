from src.core.commands import Command
from returns.result import Result
from immutables import Map

class MyApp:
    """ Main class to execute commands and command handler"""

    def __init__(self, name: str):
        self._name = name


    async def execute(
            self, obj: Command, result_map: Map = Map()
    )-> Result:
        _cls = type(obj)
        if issubclass(obj, Command):...
