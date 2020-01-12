"""Host config object."""
from contextlib import asynccontextmanager

from aiolxd import Client
from pofy import StringField

from cchoir.lib.config import Config

class Host:
    """Host config object.

    Hosts are deployment targets, serving the LXD api.
    """

    class Schema:
        """Pofy fields."""

        url = StringField()

    def __init__(self):
        self.url: str = 'http://localhost:8443'
        config = Config.load()

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

    async def authenticate(self, password):
        config = Config.load()
        cert_path = config.client_certificate
        async with self._get_api() as api:
            if api.auth == "trusted":
                return
            certificates = api.certificates
            await certificates.add(password, cert_path)
