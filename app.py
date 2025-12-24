
from dataclasses import dataclass
from xml.sax import handler
from returns.result import Result
from typing import Callable
from di import Container
from immutables import Map
import inspect
from typing import Any, Type

#application/commands.py
class Command:
    
    def __post_init__(self):
        self._result : Result | None = None

    def set_result(self, result: Any):
        self._result = result

    def get_result(self) -> Result | None:
        return self._result

#application/main.py
class Module:
    """ """

    def __init__(self, name):
        self.name = name
        self._handlers: dict[Type[Command], Callable] = {}
        self._bindings: list[tuple] = []

    def register_handler(self, handler_func: Callable):
        # Registering {handler_func.__name}
        sig = inspect.signature(handler_func)
        param_cls = sig.parameters['cmd'].annotation
        if not issubclass(param_cls,Command):
            raise ValueError("Error Registering {handler_func.__name__}")
        self._handlers[param_cls] = handler_func

    def get_handler(self, command_type: Command):
        return self._handlers.get(command_type)
    
    def bind_subtype(self, subtype, _type):
        #like here it is making a tuple of implementation repo with repo
        self._bindings.append((subtype,_type))

    @property
    def handlers(self):
        return self._handlers


class Appication(Module):
    """
    """

    def __init__(self, name):
        super().__init__(name)
        self.__modules: set[Module] = set([self])
        self._container = Container()
        self._solved_dependencies = {}



    def include_module(self, module: Module):
        """Include module into application"""
        self.__modules.add(module)

        # registering all module handlers
        self._handlers.update(module.handlers)
        # for cmd_type, handler in module._handlers.items():
        #     self.register_handler(cmd_type,handler)

        # bind dependencies
        for bindings in module._bindings:
            self._container.bind(*binding)

    def solve_dependencies(self):
        """Resolve dependencies for all modules"""
        for module in self._modules:
            for subtype, _type in module._bindings:
                self._solved_dependencies[_type]=self._container.resolve(_type)



    def execute(self, command: Command, result_map: Map= Map()):
        """Find the handler and execute with dependencies"""
        handler = self.get_handler(type(command))
        if not handler:
            raise ValueError(f"No handler registered for {type(command).__name__}")
        sig = inspect.signature(handler)

        # build kwargs for handler
        kwargs = {}
        for name, param in sig.parameters.items():
            if param.annotation in self._solved_dependencies:
                kwargs[name] = self._solved_dependencies[param.annotation]
            elif param == "cmd":
                kwargs[param] = command
            elif param == "result_map":
                kwargs[param] = result_map
    
        return handler(command, **kwargs)


@dataclass
class PrintAnyCommand(Command):
    text: str | None = None
    
def print_any_handler(cmd: PrintAnyCommand):
    print(f"printing {cmd.text}")
    result = cmd.text
    cmd.set_result(result)
    return result


test = Module("test")
test.register_handler(print_any_handler)



app = Appication("MainApp")
app.include_module(test)

app.execute(PrintAnyCommand("Hello sujish @@@@@"))