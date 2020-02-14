"""Helpers for using aiolxd Instance endpoint."""
from shlex import split
from typing import Any
from typing import Awaitable
from typing import Generator
from typing import List

from aiolxd import Instance


class InstanceWrapper:
    """Wrapper around the aiolxd instance object."""

    def __init__(self, lxd_instance: Instance) -> None:
        """Initialize the instance."""
        self._lxd_instance = lxd_instance

    def __call__(self, command_format: str, *args: str, **kwargs: str) \
            -> Awaitable[str]:
        command = command_format.format(*args, **kwargs)
        splitted_command = split(command)
        return _CallAwaitable(self._lxd_instance, splitted_command)


class _CallAwaitable:
    def __init__(self, lxd_instance: Instance, command: List[str]):
        self._lxd_instance = lxd_instance
        self._command = command

    def __await__(self) -> Generator[None, Any, str]:
        return self._process().__await__()

    async def _process(self) -> str:
        return ''
