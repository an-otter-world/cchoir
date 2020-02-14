"""Deploy command module."""
from argparse import ArgumentParser
from argparse import Namespace

from cchoir.commands.command import Command
from cchoir.commands.common import load_site


class DeployCommand(Command):
    """Deploys a site to LXD hosts."""

    name = 'deploy'

    def configure(self, parser: ArgumentParser) -> None:
        pass

    async def run(self, arguments: Namespace) -> bool:
        site = load_site(arguments)
        await site.deploy()
        return True
