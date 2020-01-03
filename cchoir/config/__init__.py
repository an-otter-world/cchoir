"""C-Choir config classes & utilities."""
from pathlib import Path

from pofy import load

from .site import SiteConfig


def load_config(path: Path):
    """Load a site configuration.

    Args:
        path: Path to the site config file.

    """
    site_root = path.parent
    with open(path, 'r') as config_file:
        return load(
            config_file,
            object_class=SiteConfig,
            resolve_roots=[site_root]
        )
