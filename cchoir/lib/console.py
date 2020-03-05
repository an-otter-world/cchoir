"""Helpers for using aiolxd Instance endpoint."""
from contextlib import contextmanager
from shlex import split
from typing import Any
from typing import Awaitable
from typing import Dict
from typing import Generator
from typing import IO
from typing import Iterator
from typing import List
from typing import Optional

from aiolxd import Instance

from cchoir.lib.log import Log


class Console:
    """Wrapper around the aiolxd instance object to execute commands."""

    def __init__(self, lxd_instance: Instance, log: Log) -> None:
        """Initialize the instance."""
        self._lxd_instance = lxd_instance
        self._env: Optional[Dict[str, str]] = None
        self._stdout: Optional[IO[bytes]] = None
        self._stderr: Optional[IO[bytes]] = None
        self.log = log

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
        self.log.warning('Executing %s', command)
        splitted_command = split(command)
        return _CallAwaitable(
            lxd_instance=self._lxd_instance,
            log=self.log,
            command=splitted_command,
            env=self._env,
            stdout=self._stdout,
            stderr=self._stderr
        )


class _CallAwaitable:
    def __init__(
        self,
        lxd_instance: Instance,
        log: Log,
        command: List[str],
        env: Optional[Dict[str, str]],
        stdout: Optional[IO[bytes]],
        stderr: Optional[IO[bytes]],
    ) -> None:
        self._lxd_instance = lxd_instance
        self.log = log
        self._command = command
        self._env = env
        self._stdout = stdout
        self._stderr = stderr

    def __await__(self) -> Generator[None, Any, int]:
        return self._process().__await__()

    async def _process(self) -> int:

        async def stdout_callback(data: bytes) -> None:
            self.log.warning(data.decode('utf-8'))
            if self._stdout is not None:
                self._stdout.write(data)

        async def stderr_callback(data: bytes) -> None:
            self.log.error(data.decode('utf-8'))
            if self._stderr is not None:
                self._stderr.write(data)

        result = await self._lxd_instance.exec(
            self._command,
            environment=self._env,
            stdout=stdout_callback,
            stderr=stderr_callback
        )

        return int(result["metadata"]["return"])
