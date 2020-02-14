"""Site configuration class & utilities."""
from asyncio import gather
from gettext import gettext as _
from logging import getLogger
from pathlib import Path
from typing import cast
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Pattern

from pofy import DictField
from pofy import ObjectField
from pofy import load

from cchoir.lib.config import Config
from cchoir.lib.host import Host

_LOG = getLogger(__name__)


class Site:
    """Site configuration object."""

    class Schema:
        """Pofy fields."""

        hosts = DictField(ObjectField(object_class=Host))

    def __init__(self) -> None:
        """Initialize the host."""
        self.hosts: Dict[str, Host] = {}

    @staticmethod
    def load(path: Path) -> 'Site':
        """Load the site config object.

        Args:
            path: Path to the site yaml config file.

        """
        with open(path, 'r') as site_file:
            site_content = site_file.read()
            return cast(Site, load(site_content, Site))

    async def deploy(self, container_pattern: Optional[Pattern[str]] = None) \
            -> None:
        """Deploy all containers matching the given pattern.

        Args:
            container_pattern: Pattern container to be deployed must match.

        """
        config = Config.load()
        await gather(*[
            host.deploy(config, container_pattern)
            for host in self.get_hosts()
        ])

    def get_hosts(self, names: Optional[Iterable[str]] = None) \
            -> Iterable[Host]:
        """Get hosts with the given names.

        Args:
            names: Names of hosts to get.

        Return:
            Iterable of retrieved hosts.

        """
        hosts = self.hosts
        if names is None:
            return hosts.values()

        result = []
        for name_it in names:
            host = hosts.get(name_it)
            if host is None:
                _LOG.error(_("Unknown host {}"), name_it)
                continue
            result.append(host)
        return result
