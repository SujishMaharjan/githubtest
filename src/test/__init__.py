from src.core.handlers import CommandHandlers
from src.test.handlers import print_any_test


test_handler = CommandHandlers("test")


test_handler.handler(print_any_test)