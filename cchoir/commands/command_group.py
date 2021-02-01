"""Command aggregating several subcommands."""
from argparse import ArgumentParser
from argparse import Namespace
from typing import List

from cchoir.commands.command import Command
from cchoir.commands.common import configure_subcommands
from cchoir.commands.common import run_subcommand


class CommandGroup(Command):
    """Command aggregating several subcommands."""

    def __init__(self, sub_commands: List[Command]):
        """Construct a group command."""
        self._sub_commands = sub_commands
        self._subparser_id = self.name + '_subcommand'

    def configure(self, parser: ArgumentParser) -> None:
        configure_subcommands(
            self._sub_commands,
            parser,
            self._subparser_id
        )

    async def run(self, arguments: Namespace) -> bool:
        return await run_subcommand(
            self._sub_commands,
            arguments,
            self._subparser_id
        )
