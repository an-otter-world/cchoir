"""Deploy command module."""
from argparse import ArgumentParser
from argparse import Namespace
from logging import getLogger

from cchoir.commands.command import Command
from cchoir.commands.common import load_site
from cchoir.lib.config import Config
from cchoir.lib.ssl import gen_certificate

_LOG = getLogger(__name__)


class CertCreateCommand(Command):
    """Creates a certificate."""

    name = 'create'

    def configure(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '--overwrite',
            help='Overwrites existing certificate',
            action='store_true',
            default=False
        )

    async def run(self, arguments: Namespace) -> bool:
        config = Config.load()
        if config is None:
            return False

        certificate = config.certificate
        if certificate.exists() and not arguments.overwrite:
            _LOG.error('Certificate already exists : %s', certificate)
            return False

        gen_certificate(
            config.key,
            config.certificate,
            4096
        )

        return True
