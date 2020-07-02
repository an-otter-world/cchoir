"""Empty debian container instance template."""
from contextlib import asynccontextmanager
from typing import AsyncIterator
from typing import List

from pofy import ListField
from pofy import StringField

from cchoir.lib.instance import Instance
from cchoir.lib.instance_console import InstanceConsole


class Base(Instance):
    """Base template for Debian based instances."""

    class Schema:
        """Pofy fields."""

        packages = ListField(StringField())

    def __init__(self) -> None:
        """Initialize Debian instance."""
        super().__init__()
        self.packages: List[str] = []

    @asynccontextmanager
    async def _setup(self, shell: InstanceConsole) -> AsyncIterator[None]:
        with shell.use(env={'DEBIAN_FRONTEND': 'noninteractive'}):
            await shell('bash -c "apt-mark showmanual   | xargs apt-mark auto"')
            await shell('apt-get -y install {}', ' '.join(self.packages),)
            yield
            shell('apt-get -y -qq autoremove --purge')

    @asynccontextmanager
    async def _update(self, shell: InstanceConsole) -> AsyncIterator[None]:
        await shell('apt-get -y -qq update')
        await shell('apt-get -y -qq dist-upgrade')
        yield
