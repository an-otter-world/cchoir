"""C-Choir core classes & utilities."""
from pathlib import Path
from typing import cast

from pofy import load

from cchoir.lib.site import Site


def load_site(path: Path) -> Site:
    """Load a site configuration.

    Args:
        path: Path to the site config file.

    """
    site_root = path.parent
    with open(path, 'r') as config_file:
        return cast(Site, load(
            config_file,
            object_class=Site,
            resolve_roots=[site_root]
        ))
