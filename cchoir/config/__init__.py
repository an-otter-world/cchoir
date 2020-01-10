"""C-Choir config classes & utilities."""
from pathlib import Path
from typing import cast

from pofy import load

from cchoir.config.site import SiteConfig


def load_config(path: Path) -> SiteConfig:
    """Load a site configuration.

    Args:
        path: Path to the site config file.

    """
    site_root = path.parent
    with open(path, 'r') as config_file:
        return cast(SiteConfig, load(
            config_file,
            object_class=SiteConfig,
            resolve_roots=[site_root]
        ))
