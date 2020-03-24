"""Helpers for using aiolxd Instance endpoint."""
from contextlib import contextmanager
from pathlib import Path
from shlex import split
from string import Template
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import Generator
from typing import IO
from typing import Iterator
from typing import List
from typing import Optional

from aiolxd import Instance

from cchoir.lib.log import Log


class CommandException(Exception):
    """Exception raised when a command fails."""

    def __init__(self, command: str, return_code: int) -> None:
        """Initialize the exception.

        Args:
            command: The command that failed.
            return_code: Return code of the command.

        """
        super().__init__('Command %s failed.' % command)
        self.command = command
        self.return_code = return_code


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
        self.log.info('Executing %s', command)
        splitted_command = split(command)
        return _CallAwaitable(
            lxd_instance=self._lxd_instance,
            log=self.log,
            command=splitted_command,
            env=self._env,
            stdout=self._stdout,
            stderr=self._stderr
        )

    def expand(
        self,
        template_path: Path,
        target_path: Path,
        uid: int = 0,
        gid: int = 0,
        mode: str = '0700'
    ) -> None:
        """Expand a configuration template in the runnig instance."""
        with open(template_path, 'r') as template_file:
            template = Template(template_file.read())

            expanded_file = template.substitute({
                'instance': self._lxd_instance.status
            })
            with self._lxd_instance.open(
                target_path,
                'w',
                uid=uid,
                gid=gid,
                mode=mode
            ) as instance_file:
                instance_file.write(expanded_file)


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
        stdout_buffer: str = ''
        stderr_buffer: str = ''

        def _log(buffer: str, data: bytes, callback: Callable[[str], None])\
                -> str:
            buffer += data.decode('utf-8')

            if len(buffer) == 0:
                return ''

            lines = buffer.strip().split('\n')
            if buffer[-1] != '\n':
                buffer = lines[-1]
                lines = lines[:-1]
            else:
                buffer = ''

            for line in lines:
                callback(line)

            return buffer

        async def stdout_callback(data: bytes) -> None:
            nonlocal stdout_buffer
            stdout_buffer = _log(stdout_buffer, data, self.log.info)

            if self._stdout is not None:
                self._stdout.write(data)

        async def stderr_callback(data: bytes) -> None:
            nonlocal stderr_buffer
            stderr_buffer = _log(stderr_buffer, data, self.log.warning)
            if self._stderr is not None:
                self._stderr.write(data)

        result = await self._lxd_instance.exec(
            self._command,
            environment=self._env,
            stdout=stdout_callback,
            stderr=stderr_callback
        )

        return_value = int(result["metadata"]["return"])
        if return_value != 0:
            raise CommandException(' '.join(self._command), return_value)

        return return_value
