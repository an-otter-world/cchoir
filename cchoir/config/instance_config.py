"""Instance config object."""
from abc import ABC
from abc import abstractmethod
from contextlib import asynccontextmanager
from logging import getLogger
from logging import Logger
from typing import AsyncIterator

from aiolxd import Api
from aiolxd import Source
from pofy import StringField


class Instance(ABC):
    """Instance config object."""

    class Schema:
        """Pofy fields."""

        name = StringField(required=True)

    def __init__(self) -> None:
        """Initialize the instance."""
        self.name: str = ''
