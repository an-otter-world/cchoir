"""Host config object."""
from contextlib import asynccontextmanager
from typing import Optional

from pofy import StringField
from aiolxd import Client

from cchoir.lib.config import Config


class Host:
    """Host config object.

    Hosts are deployment targets, serving the LXD api.
    """

    class Schema:
        """Pofy fields."""

        url = StringField()

    def __init__(self) -> None:
        """Initialize the host."""
        self.url: str = 'http://localhost:8443'

    def deploy(self, container_pattern: Optional[str]) -> None:
        """Deploy containers matching the given pattern."""

    @asynccontextmanager
    async def _get_api(self) -> Client:
        config = Config.load()
        async with Client(
            base_url=self.url,
            client_cert=config.client_certificate,
            client_key=config.client_key,
            verify_host_certificate=False
        ) as client:
            async with client.api as api:
                yield api
