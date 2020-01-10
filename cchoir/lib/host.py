"""Host config object."""
from pofy import StringField


class Host:
    """Host config object.

    Hosts are deployment targets, serving the LXD api.
    """

    class Schema:
        """Pofy fields."""

        address = StringField()
