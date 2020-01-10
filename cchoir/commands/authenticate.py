"""Authenticate command module."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _

from cchoir.commands.command import Command


class AuthenticateCommand(Command):
    """Authenticate against the hosts configured in the site."""

    name = 'authenticate'

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '--password',
            help=_('The trusted_user_password to use to register the '
                   'client certficate.')
        )

    def run(self, arguments: Namespace) -> bool:
        pass
