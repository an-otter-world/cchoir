"""Instance config object."""
from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncIterator
from typing import Optional

from aiolxd import Api
from aiolxd import Source
from pofy import StringField

from cchoir.lib.console import Console
from cchoir.lib.log import Log


class Instance(ABC):
    """Instance config object."""

    class Schema:
        """Pofy fields."""

        name = StringField(required=True)

        @classmethod
        def post_load(cls, instance: 'Instance') -> None:
            """Set up the log when the instance is loaded from YAML.

            Needed as the name member is defined in YAML.

            """
            instance.log = Log('instances.{}'.format(instance.name))
            instance._post_load() # pylint: disable=protected-access

    def __init__(self) -> None:
        """Initialize the instance."""
        self.name: str = ''
        self.log: Optional[Log] = None

    async def deploy(self, api: Api) -> None:
        """Deploy this container."""
        lxd_instances = await api.instances()
        name = self.name
        if name not in lxd_instances:
            lxd_instance = await lxd_instances.create(
                name,
                'x86_64',
                ephemeral=False,
                source=Source(
                    instance_type=Source.Type.IMAGE,
                    mode=Source.Mode.PULL,
                    protocol=Source.Protocol.SIMPLESTREAMS,
                    server='https://cloud-images.ubuntu.com/daily',
                    alias='16.04'
                )
            )
        else:
            lxd_instance = await lxd_instances[name]

        if lxd_instance.status != 'Running':
            await lxd_instance.start()

        assert self.log is not None
        console = Console(lxd_instance, self.log)
        async with self._setup(console):
            async with self._update(console):
                pass

    def _post_load(self) -> None:
        pass

    @abstractmethod
    @asynccontextmanager
    async def _setup(self, shell: Console) -> AsyncIterator[None]:
        yield

    @abstractmethod
    @asynccontextmanager
    async def _update(self, shell: Console) -> AsyncIterator[None]:
        yield
