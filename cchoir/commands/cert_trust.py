"""Deploy command module."""
from argparse import ArgumentParser
from argparse import Namespace

from cchoir.commands.command import Command
from cchoir.commands.common import load_site


class CertTrustCommand(Command):
    """Trusts the currently configured certificate."""

    name = 'trust'

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '--hosts',
            help='Hosts for which to add the certificate as trusted',
            nargs='*'
        )

        parser.add_argument(
            '--trust-password',
            help='The LXD trust password to use to add trusted certificates'
        )

    async def run(self, arguments: Namespace) -> bool:
        site = load_site(arguments)
        return await site.trust(
            arguments.hosts,
            arguments.trust_password
        )
