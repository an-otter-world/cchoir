"""Instance config object."""
from pofy import StringField
from aiolxd import Api


class Instance:
    """Instance config object."""

    class Schema:
        """Pofy fields."""

        name = StringField(required=True)

    def __init__(self) -> None:
        """Initialize the instance."""
        self.name: str = ''

    def deploy(self, api: Api) -> None:
        """Deploy this container."""
        raise NotImplementedError
