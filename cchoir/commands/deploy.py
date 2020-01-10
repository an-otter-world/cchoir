"""Deploy command module."""
from argparse import ArgumentParser
from argparse import Namespace

from cchoir.commands.command import Command


class DeployCommand(Command):
    """Deploys a site to LXD hosts."""

    name = 'deploy'

    def configure(self, parser: ArgumentParser) -> None:
        pass

    def run(self, arguments: Namespace) -> bool:
        pass
