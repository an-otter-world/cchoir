"""DNS server debian container instance template."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator
from typing import Optional

from pofy import PathField

from cchoir.lib.console import Console
from cchoir.instances.debian.base import Base


class Dns(Base):
    """Template for Debian based DNS Server."""

    class Schema:
        """Pofy fields."""

        configuration = PathField()

    def __init__(self) -> None:
        """Initialize Debian instance."""
        super().__init__()
        self.configuration: Optional[Path] = None

    @asynccontextmanager
    async def _setup(self, shell: Console) -> AsyncIterator[None]:
        assert self.configuration is not None
        shell.expand(self.configuration, Path('/etc/bind/named.conf'))
        yield

    @asynccontextmanager
    async def _update(self, shell: Console) -> AsyncIterator[None]:
        yield

    def _post_load(self) -> None:
        super()._post_load()
        self.packages += ['bind9']
