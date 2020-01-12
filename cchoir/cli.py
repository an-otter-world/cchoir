"""C-Choir command line entry point."""
from sys import argv
from sys import exit as sys_exit
from asyncio import run

from cchoir.commands import configure


def main() -> int:
    """C-Choir entry point."""
    command, arguments = configure(argv[1:])
    if run(command.run(arguments)):
        return 0

    return 1


if __name__ == '__main__':
    RESULT = main()
    sys_exit(RESULT)
