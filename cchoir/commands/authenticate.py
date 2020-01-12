"""Authenticate command module."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _
from pathlib import Path

from cchoir.commands.command import Command
from cchoir.lib import load_site


class AuthenticateCommand(Command):
    """Authenticate against the hosts configured in the site."""

    name = 'authenticate'

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '--password',
            help=_('The trusted_user_password to use to register the '
                   'client certficate.'),
            required=True
        )

    async def run(self, arguments: Namespace) -> bool:
        site_path = Path(arguments.site)
        site = load_site(site_path)
        for host in site.get_hosts():
            await host.authenticate(arguments.password)
        return True
