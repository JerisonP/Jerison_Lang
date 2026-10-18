from jerison_lang.scanner import Scanner, Token
import jerison_lang.constants as const
from jerison_lang import error as err
import sys

def run(source: str) -> bool:
    scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()

    # For debugging just print tokens
    for token in tokens:
        print(token)

    return False


def run_file(file_name: str, had_error: list[bool]) -> None:
    with open(file_name, "rb") as file:
        source = file.read().decode(const.DEFAULT_CHARACTER_SET)
    
    had_error[0] = run(source)
    if had_error[0]:
        sys.exit(err.COMMAND_LINE_USAGE_ERROR)


def run_prompt(had_error: list[bool]) -> None:
    while True:
        try:
            line = input("> ")
        except EOFError:
            return
        had_error[0] = run(line)
        had_error[0] = False