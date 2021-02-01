"""Host config object."""
from asyncio import gather
from contextlib import asynccontextmanager
from typing import List
from typing import Optional
from typing import Pattern

from aiolxd import Api
from aiolxd import lxd_api

from pofy import BoolField
from pofy import ListField
from pofy import ObjectField
from pofy import StringField

from cchoir.lib.config import Config
from cchoir.lib.instance import Instance


class Host:
    """Host config object.

    Hosts are deployment targets, serving the LXD api.
    """

    class Schema:
        """Pofy fields."""

        url = StringField()
        verify_host_certificate = BoolField()
        instances = ListField(
            item_field=ObjectField(Instance)
        )

    def __init__(self) -> None:
        """Initialize the host."""
        self.url: str = 'https://localhost:8443'
        self.verify_host_certificate = False
        self.instances: List[Instance] = []

    async def deploy(self, config: Config, pattern: Optional[Pattern[str]]) \
            -> None:
        """Deploy instances matching the given pattern."""
        async with self._get_api(config) as api:
            await gather(*[
                instance.deploy(api)
                for instance in self.instances
                if pattern is None or pattern.match(instance.name)
            ])

    async def trust(
        self,
        config: Config,
        trust_password: Optional[str] = None
    ) \
            -> None:
        """Add the current certificate to the trusted ones."""
        async with self._get_api(config) as api:
            if api.is_client_trusted:
                return False

            await api.add_certificate(
                cert_path=config.certificate,
                password=trust_password
            )

    @asynccontextmanager
    async def _get_api(self, config: Config) -> Api:
        async with lxd_api(
            base_url=self.url,
            verify_host_certificate=False,
            client_key=config.key,
            client_cert=config.certificate,
        ) as api:
            yield api
