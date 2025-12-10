from src.test.commands import PrintAnyCommand


def print_any_test(
        cmd: PrintAnyCommand
):
    print(f"{cmd.text}")