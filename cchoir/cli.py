"""C-Choir command line entry point."""
from asyncio import run
from logging import basicConfig
from logging import INFO
from sys import argv
from sys import exit as sys_exit

from cchoir.commands.cert import CertCommand
from cchoir.commands.deploy import DeployCommand
from cchoir.commands.common import run as run_command


def main() -> int:
    """C-Choir entry point."""
    basicConfig(level=INFO)
    if run(run_command(
        argv[1:],
        CertCommand(),
        DeployCommand()
    )):
        return 0

    return 1


if __name__ == '__main__':
    RESULT = main()
    sys_exit(RESULT)
