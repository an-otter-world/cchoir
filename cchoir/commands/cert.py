"""Certificate related commands."""
from cchoir.commands.cert_create import CertCreateCommand
from cchoir.commands.cert_trust import CertTrustCommand
from cchoir.commands.command_group import CommandGroup


class CertCommand(CommandGroup):
    """Client-side certificate related commands."""

    name = 'cert'

    def __init__(self) -> None:
        """Construct a CertCommand."""
        super().__init__([
            CertCreateCommand(),
            CertTrustCommand()
        ])
