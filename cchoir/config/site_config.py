"""Site configuration class & utilities."""
from typing import Dict

from pofy import DictField
from pofy import ObjectField
from pofy import StringField

from cchoir.config.host_config import Host


class SiteConfig:
    """Site configuration object."""

    class Schema:
        """Pofy fields."""

        hosts = DictField(ObjectField(object_class=HostConfig))
        name = StringField(required=True)

    def __init__(self) -> None:
        """Initialize the host."""
        self.hosts: Dict[str, HostConfig] = {}
        self.name: str = ""
