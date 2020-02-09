"""Config helpers."""
from pathlib import Path

from appdirs import user_config_dir
from pofy import PathField
from pofy import load


class Config:
    """C-Choir configuration class."""

    class Schema:
        """Pofy fields."""

        client_certificate = PathField()
        client_key = PathField()

    @staticmethod
    def load() -> 'Config':
        """Load the user-defined config."""
        config_file_path = Config._get_config_dir() / 'config.yaml'
        if config_file_path.exists():
            config = load(config_file_path, Config)
        else:
            config = Config()

        assert isinstance(config, Config)
        return config

    def __init__(self) -> None:
        """Initialize the config.

        Give default value to config values here.
        """
        self.client_certificate: Path = self._get_config_dir() / 'client.cert'
        self.client_key: Path = self._get_config_dir() / 'client.key'

    @staticmethod
    def _get_config_dir() -> Path:
        return Path(user_config_dir('cchoir'))
