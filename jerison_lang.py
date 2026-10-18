import jerison_lang as jlang
from jerison_lang import constants as const
import sys


def valid_extension(file_name: str) -> bool:
    return file_name.endswith(const.FILE_EXTENSION)


def read_bytes(file_name: str) -> bytes:
    with open(file_name, "rb") as file:
        data = file.read()
    return data


def run(text: str) -> None:
    pass


def run_file(file_name: str) -> None:
    source = read_bytes(file_name).decode(const.DEFAULT_CHARACTER_SET, errors="strict")
    run(source)


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
        except EOFError:
            return None
        run(line)


if __name__ == "__main__":
    # Validate user input of file
    len_args = len(sys.argv)
    if len_args > 2:
        raise ValueError(
            f"too many arguments where give. no more then one was expected but {len_args - 1} was given"
        )
    # Run file
    elif len_args == 2:
        file_name = sys.argv[1]
        if not valid_extension(file_name):
            raise ValueError(
                f"file with the extension {const.FILE_EXTENSION} was expected"
            )
        run_file(file_name)
    # Interactive mode
    else:
        run_prompt()
