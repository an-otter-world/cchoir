"""Config helpers."""
from logging import getLogger
from pathlib import Path

# As the import is used in a string for the typing system, pylint incorrectly
# sees it as unused
from typing import Optional # pylint: disable=unused-import

from appdirs import user_config_dir
from pofy import load


# TODO: Rename this to LocalConfig, it's confusing.
class Config:
    """C-Choir configuration class."""

    class Schema:
        """Pofy fields."""

    @staticmethod
    def load() -> 'Optional[Config]':
        """Load the user-defined config."""
        config_file_path = Config._get_config_dir() / 'config.yaml'
        if config_file_path.exists():
            config = load(config_file_path, Config)
        else:
            config = Config()

        assert isinstance(config, Config)

        logger = getLogger('cchoir.core')
        if not config.key.exists():
            logger.error(
                'Unable to find your client certificate key %s to'
                ' authenticate to the LXD api, please save before'
                ' launching C-Choir',
                config.key
            )
            return None
        if not config.certificate.exists():
            logger.error(
                'Unable to find your client certificate key %s to'
                ' authenticate to the LXD api, please save before'
                ' launching C-Choir',
                config.certificate
            )
            return None

        logger.debug('Loaded config file')
        return config

    def __init__(self) -> None:
        """Initialize the config.

        Give default value to config values here.
        """
        self.certificate: Path = self._get_config_dir() / 'certificate.pem'
        self.key: Path = self._get_config_dir() / 'key.pem'

    @staticmethod
    def _get_config_dir() -> Path:
        return Path(user_config_dir('cchoir'))
