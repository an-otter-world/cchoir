"""Empty debian container instance template."""
from contextlib import asynccontextmanager
from typing import AsyncIterator
from typing import List

from pofy import ListField
from pofy import StringField

from cchoir.lib.instance import Instance
from cchoir.lib.console import Console


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
    async def _setup(self, shell: Console) -> AsyncIterator[None]:
        with shell.use(env={'DEBIAN_FRONTEND': 'noninteractive'}):
            with shell.log.step('install_packages', 'Installing packages'):
                await shell('bash -c "apt-mark showmanual |'
                            ' xargs apt-mark auto"')
                await shell('apt-get -y install {}', ' '.join(self.packages),)
                yield
            with shell.log.step('clean_packages', 'Cleaning packages'):
                await shell('apt-get -y -qq autoremove --purge')

    @asynccontextmanager
    async def _update(self, shell: Console) -> AsyncIterator[None]:
        with shell.log.step('update_packages', 'Updating packages'):
            await shell('apt-get -y -qq update')
            await shell('apt-get -y -qq dist-upgrade')
        yield
