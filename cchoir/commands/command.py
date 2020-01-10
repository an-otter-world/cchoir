"""Command base class & utilities."""
from abc import abstractmethod
from argparse import ArgumentParser
from argparse import Namespace


class Command:
    """Base class for a C-Choir command."""

    name: str = ''

    @abstractmethod
    def configure(self, parser: ArgumentParser) -> None:
        """Configure command line arguments for this command.

        Args:
            parser (ArgumentParser) : The argument parser.

        """
        raise NotImplementedError()

    @abstractmethod
    def run(self, arguments: Namespace) -> bool:
        """Run the command.

        Args:
            arguments: Command line arguments configured in configure method.

        """
        raise NotImplementedError()
