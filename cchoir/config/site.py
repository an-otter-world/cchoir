"""Site configuration class & utilities."""
from pofy import DictField
from pofy import ObjectField

from .host import HostConfig


class SiteConfig:
    """Site configuration object."""

    class Schema:
        """Pofy fields."""

        hosts = DictField(ObjectField(object_class=HostConfig))
