"""Command line common utilites & helpers."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _
from pathlib import Path
from typing import List

from cchoir.commands.command import Command
from cchoir.lib.errors import CChoirException
from cchoir.lib.site import Site


def load_site(arguments: Namespace) -> Site:
    """Load the site config object.

    Args:
        arguments: Namespace returned by arguments parser configured with the
                   configure_common_arguments function.

    """
    site_path = arguments.site
    if site_path is None:
        site_path = Path.cwd() / 'site.yaml'
        if not site_path.is_file():
            raise CChoirException(_(
                'Unable to find a "site.yaml" configuration file in the '
                'working directory. Check you launch cchoir from the good '
                'directory, or specify the site file with the --site '
                'command line parameter'))
    return Site.load(site_path)


def configure_common_arguments(parser: ArgumentParser) -> None:
    """Configure the commonly used arguments on the command line."""
    parser.add_argument(
        '--site',
        help='Path to the site configuration file (in YAML format)',
        default=None
    )


def configure_subcommands(
    commands: List[Command],
    parser: ArgumentParser,
    subparser_id: str
) -> None:
    """Configure command arguments in the given parser.

    Args:
        commands: List of commands to configure.
        parser: Argument parser to configure.
        subparser_id: Unique string identifier for the subparser.

    """
    subparsers = parser.add_subparsers(
        help='Subcommand to run.',
        dest=subparser_id,
    )

    for command_it in commands:
        command_parser = subparsers.add_parser(
            name=command_it.name,
            description=command_it.__class__.__doc__,
            help=command_it.__class__.__doc__,
        )
        command_it.configure(command_parser)


async def run_subcommand(
    commands: List[Command],
    arguments: Namespace,
    subparser_id: str
) -> bool:
    """Run the commands prior configured with configure_subcommands.

    Args:
        commands: List of commands to configure.
        parser: Argument parser to configure.
        arguments: List of arguments to parse.
        subparser_id: Unique string identifier for the subparser.

    Return:
        bool: result of the ran command.

    """
    command_name = getattr(arguments, subparser_id)
    command = next(it for it in commands if it.name == command_name)
    return await command.run(arguments)


async def run(arguments: List[str], *commands: Command) -> bool:
    """Configure and run command.

    Args:
        commands (List[Command]) : List of commands to configure.
        arguments (List[str]) : Command line arguments to parse.

    Return:
        bool: result of the ran command.

    """
    parser = ArgumentParser()

    configure_common_arguments(parser)

    configure_subcommands(list(commands), parser, 'cchoir')
    parsed_args = parser.parse_args(arguments)
    return await run_subcommand(list(commands), parsed_args, 'cchoir')
