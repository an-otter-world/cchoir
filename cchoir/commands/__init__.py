"""C-Choir commands module."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _
from typing import List
from typing import Tuple

from cchoir.commands.authenticate import AuthenticateCommand
from cchoir.commands.command import Command
from cchoir.commands.deploy import DeployCommand


def configure(arguments: List[str]) -> Tuple[Command, Namespace]:
    """Load command line argument parser and parse arguments.

    Args:
        arguments (List[str]) : Command line arguments to parse.

    Return:
        command, arguments (Command, Namespace) : The selected command and
                                                  parsed arguments.

    """
    parser = ArgumentParser()
    commands = [
        AuthenticateCommand(),
        DeployCommand()
    ]

    command_index = {it.name: it for it in commands}

    subparsers = parser.add_subparsers(
        help='C-Choir command to run.',
        dest='selected_command',
    )

    for command_it in commands:
        command_parser = subparsers.add_parser(
            name=command_it.name,
            description=command_it.__class__.__doc__,
            help=command_it.__class__.__doc__,
        )
        command_it.configure(command_parser)

    parser.add_argument(
        '--site',
        help=_('Site definition to load'),
        default='site.yaml'
    )

    parsed_args = parser.parse_args(arguments)
    command_name = parsed_args.selected_command
    command = command_index[command_name]

    return (command, parsed_args)
