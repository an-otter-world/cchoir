"""Instance config object."""
from aiolxd import Api
from aiolxd import Source
from pofy import StringField


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
        instances = await api.instances()
        name = self.name
        if name not in instances:
            instance = await instances.create(
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
            instance = await instances[name]

        instance('echo "test"')
