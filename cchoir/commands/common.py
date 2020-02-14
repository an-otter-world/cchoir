"""Command line common utilites & helpers."""
from argparse import ArgumentParser
from argparse import Namespace
from gettext import gettext as _
from pathlib import Path

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
