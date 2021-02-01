"""C-Choir commands module."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _
from typing import List
from typing import Tuple

from cchoir.commands.cert import CertCommand
from cchoir.commands.command import Command
from cchoir.commands.common import configure_common_arguments
from cchoir.commands.common import configure_subcommands
from cchoir.commands.common import run_subcommand
from cchoir.commands.deploy import DeployCommand


async def run(arguments: List[str]) -> bool:
    """Load command line argument parser and parse arguments.

    Args:
        arguments (List[str]) : Command line arguments to parse.

    Return:
        command, arguments (Command, Namespace) : The selected command and
                                                  parsed arguments.

    """
    parser = ArgumentParser()

    configure_common_arguments(parser)

    commands = [
        CertCommand(),
        DeployCommand(),
    ]

    configure_subcommands(commands, parser, 'cchoir')
    parsed_args = parser.parse_args(arguments)
    return await run_subcommand(commands, parsed_args, 'cchoir')
