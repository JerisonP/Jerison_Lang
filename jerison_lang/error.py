import sys

COMMAND_LINE_USAGE_ERROR = 63
CANT_OPEN_INPUT = 65


def report(line: int, where: str, message: str) -> bool:
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)
    return True


def error(line: int, message: str) -> bool:
    return report(line, "", message)
