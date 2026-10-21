import sys
from pathlib import Path

from jerison_lang import constants as const
from jerison_lang import error as err
from jerison_lang import runner as run


def valid_extension(file_name: str) -> bool:
    return file_name.endswith(const.FILE_EXTENSION)


if __name__ == "__main__":
    had_error = False
    len_args = len(sys.argv)
    if len_args > 2:
        print("Usage: jerison_lang <file>.jlang", file=sys.stderr)
        sys.exit(err.COMMAND_LINE_USAGE_ERROR)
    elif len_args == 2:
        file_name = sys.argv[1]
        if not valid_extension(file_name):
            print(
                f"Error: file must have a {const.FILE_EXTENSION} extension",
                file=sys.stderr,
            )
            sys.exit(err.COMMAND_LINE_USAGE_ERROR)
        elif not Path(file_name).exists():
            print(f"Error: file not found: {file_name}", file=sys.stderr)
            sys.exit(err.CANT_OPEN_INPUT)
        run.run_file(file_name, [had_error])
    else:
        run.run_prompt([had_error])
