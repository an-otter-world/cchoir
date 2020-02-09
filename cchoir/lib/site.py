"""Site configuration class & utilities."""
from gettext import gettext as _
from logging import getLogger
from typing import Dict
from typing import Iterable
from typing import Optional

from pofy import DictField
from pofy import ObjectField

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

    def deploy(self, container_pattern: Optional[str] = None) -> None:
        """Deploy all containers matching the given pattern.

        Args:
            container_pattern: Pattern container to be deployed must match.

        """
        for host in self.get_hosts():
            host.deploy(container_pattern)

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
