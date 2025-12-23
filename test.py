# domain/repositories.py
from abc import ABC, abstractmethod
from typing import Protocol


class UserRepository(Protocol):
    def get_by_id(self, user_id:int)-> dict:...


#infrasturcture layer implementation
#infra/db.py
class Database:
    def __init__(self):
        print("Database connected")

    def fetch_user(self, user_id:int):
        return {"id":user_id, "name":"sujish", "source": "from Database"}
    
#infra/user_repo.py
class UserPostgresRepository(UserRepository):
    def __init__(self, db: Database):
        # print("UserPostgres created")
        self.db = db
    

    def get_by_id(self, user_id:int)->dict:
        return self.db.fetch_user(user_id)
    

class UserInMemoryRepository(UserRepository):
    def get_by_id(self, user_id):
        return {"id":user_id, "name":"maharjan", "source": "from in memory"}
    


#application/commands.py
from typing import Any
class Command:
    def __post_init__(self):
        self._result : Any | None = None

    def set_result(self,result: Any):
        self._result = result

    def get_result(self)-> Any | None:
        return self._result
    


from di import Container, bind_by_type
from di.dependent import Dependent
from di.executors import SyncExecutor
from typing import Callable
import inspect
from typing import Type

container = Container()

#app scope
db_dep = Dependent(Database, scope="app")

request_dep = Dependent(UserPostgresRepository, scope = "request")
# service_dep = Dependent(GetUserProfile, scope="request")


# bindings = []
handlers= {}
solved_dependencies = {}

def register_handler(handler_func: Callable):
    print(f"Debug:Registering handler  {handler_func.__name__}")
    dependent = Dependent(handler_func)
    sig = inspect.signature(handler_func)
    param_cls = sig.parameters['cmd'].annotation
    if not issubclass(param_cls,Command):
        raise ValueError("Error Registering {handler_func.__name__}")
    dependent.scope="request"
    handlers[param_cls] = dependent
    return handler_func

def solve_dependencies(handlers:dict):
    for cls, dependent in handlers.items():
        print(f"Debug:Solving Depedencies for cls {type(cls)}")
        
        solved_dependencies[cls] = container.solve(
            dependent,
            scopes=["request"],
        )

def bind_subtype(subtype, _type):
    container.bind(
        bind_by_type(Dependent(subtype, scope="request"),_type)
    )


def execute(obj: Command):
    executor = SyncExecutor()

    with container.enter_scope("request") as request_state:
        solved_handler = solved_dependencies.get(type(obj))
        response = solved_handler.execute_sync(
            executor=executor,
            state=request_state,
        )
    return response

from dataclasses import dataclass
@dataclass
class GetUserProfile(Command):
    user_id : int | None = None

def get_user_profile_handler(
        cmd: GetUserProfile,
        repo: UserRepository 
):
    return repo.get_by_id(cmd.user_id)


register_handler(get_user_profile_handler)
# bind_subtype(UserPostgresRepository,UserRepository)
bind_subtype(UserInMemoryRepository,UserRepository)

solve_dependencies(handlers)

result=execute(obj=GetUserProfile(user_id=1))
print(result)