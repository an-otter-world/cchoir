"""Host config object."""
from typing import List

from pofy import BoolField
from pofy import ListField
from pofy import ObjectField
from pofy import StringField

from cchoir.config.instance_config import InstanceConfig


class HostConfig:
    """Host config object.

    Hosts are deployment targets, serving the LXD api.
    """

    class Schema:
        """Pofy fields."""

        url = StringField()
        verify_host_certificate = BoolField()
        instances = ListField(
            item_field=ObjectField(InstanceConfig)
        )

    def __init__(self) -> None:
        """Initialize the host."""
        self.url: str = 'https://localhost:8443'
        self.verify_host_certificate = False
        self.instances: List[InstanceConfig] = []
