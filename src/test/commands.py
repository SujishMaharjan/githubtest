from src.core.commands import Command
from src.core.handlers import CommandHandlers


class PrintAnyCommand(Command):
    text: str | None = None