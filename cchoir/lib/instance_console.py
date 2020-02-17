"""Helpers for using aiolxd Instance endpoint."""
from contextlib import contextmanager
from shlex import split
from typing import Any
from typing import Iterator
from typing import Awaitable
from typing import Dict
from typing import Generator
from typing import IO
from typing import List
from typing import Optional

from aiolxd import Instance


class InstanceConsole:
    """Wrapper around the aiolxd instance object to execute commands."""

    def __init__(self, lxd_instance: Instance) -> None:
        """Initialize the instance."""
        self._lxd_instance = lxd_instance
        self._env: Optional[Dict[str, str]] = None
        self._stdout: Optional[IO[bytes]] = None
        self._stderr: Optional[IO[bytes]] = None

    @contextmanager
    def use(
        self,
        env: Optional[Dict[str, str]] = None,
        stdout: Optional[IO[bytes]] = None,
        stderr: Optional[IO[bytes]] = None,
    ) -> Iterator[None]:
        """Scope in which specified environment, stdout & stderr will be used.

        Args:
            env: The environment for commands executed in this scope.
            stdout: Stream where to redirect stdout for commands executed in
                   this scope.
            stderr: Stream where to redirect stderr for commands executed in
                    this scope.

        """
        old_env = self._env
        old_stdout = self._stdout
        old_stderr = self._stderr

        self._env = env
        self._stdout = stdout
        self._stderr = stderr

        try:
            yield
        finally:
            self._env = old_env
            self._stdout = old_stdout
            self._stderr = old_stderr

    def __call__(self, command_format: str, *args: str, **kwargs: str) \
            -> Awaitable[int]:
        command = command_format.format(*args, **kwargs)
        splitted_command = split(command)
        return _CallAwaitable(
            lxd_instance=self._lxd_instance,
            command=splitted_command,
            env=self._env,
            stdout=self._stdout,
            stderr=self._stderr
        )


class _CallAwaitable:
    def __init__(
        self,
        lxd_instance: Instance,
        command: List[str],
        env: Optional[Dict[str, str]],
        stdout: Optional[IO[bytes]],
        stderr: Optional[IO[bytes]]
    ) -> None:
        self._lxd_instance = lxd_instance
        self._command = command
        self._env = env
        self._stdout = stdout
        self._stderr = stderr

    def __await__(self) -> Generator[None, Any, int]:
        return self._process().__await__()

    async def _process(self) -> int:
        stdout = stderr = None

        if self._stdout is not None:
            async def stdout_callback(data: bytes) -> None:
                assert self._stdout is not None
                self._stdout.write(data)
            stdout = stdout_callback

        if self._stderr is not None:
            async def stderr_callback(data: bytes) -> None:
                assert self._stderr is not None
                self._stderr.write(data)
            stderr = stderr_callback

        result = await self._lxd_instance.exec(
            self._command,
            environment=self._env,
            stdout=stdout,
            stderr=stderr
        )

        return int(result["metadata"]["return"])
