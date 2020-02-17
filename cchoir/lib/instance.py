"""Instance config object."""
from aiolxd import Api
from aiolxd import Source
from pofy import StringField

from cchoir.lib.instance_console import InstanceConsole


class Instance:
    """Instance config object."""

    class Schema:
        """Pofy fields."""

        name = StringField(required=True)

    def __init__(self) -> None:
        """Initialize the instance."""
        self.name: str = ''

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

        console = InstanceConsole(lxd_instance)
        await self._setup(console)

    async def _setup(self, console: InstanceConsole) -> None:
        pass
