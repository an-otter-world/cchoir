"""Logging utilities."""
from contextlib import contextmanager
from logging import getLogger
from typing import Any
from typing import Iterator


class Log:
    """Wrapper around Python Logger adding step support."""

    def __init__(self, namespace: str) -> None:
        """Initialize the instance.

        Args:
            namespace: Base namespace for this log.

        """
        self._namespace = namespace
        self._log = getLogger('cchoir.{}'.format(namespace))

    def debug(self, fmt: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug information.

        Args:
            fmt: Format of the string to log.
            *args, **kwargs: Arguments of format

        """
        self._log.debug(fmt, *args, **kwargs)

    def info(self, fmt: str, *args: Any, **kwargs: Any) -> None:
        """Log an info information.

        Args:
            fmt: Format of the string to log.
            *args, **kwargs: Arguments of format

        """
        self._log.info(fmt, *args, **kwargs)

    def warning(self, fmt: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning.

        Args:
            fmt: Format of the string to log.
            *args, **kwargs: Arguments of format

        """
        self._log.warning(fmt, *args, **kwargs)

    def error(self, fmt: str, *args: Any, **kwargs: Any) -> None:
        """Log an error.

        Args:
            fmt: Format of the string to log.
            *args, **kwargs: Arguments of format

        """
        self._log.warning(fmt, *args, **kwargs)

    @contextmanager
    def step(
        self,
        name: str,
        description_format: str,
        *args: Any,
        **kwargs: Any)\
            -> Iterator[None]:
        """Context manager to execute a step, used to classify logging.

        Args:
            name: Name for this step, the logging in the resulting context
                  will go through the cchoir.instance_name.step_name logger.

            description_format: Format of the step description that will be
                                displayed when the step starts.
            *args, **kwargs : Arguments to format the description string.

        """
        old_log = self._log
        logger_name = 'cchoir.{}.{}'.format(self._namespace, name)
        self._log = getLogger(logger_name)
        description = description_format.format(*args, **kwargs)
        self.info(description)
        yield
        self._log = old_log
