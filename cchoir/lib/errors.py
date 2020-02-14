"""Cchoir specific exception, and related helpers & utilities."""


class CChoirException(Exception):
    """Exception class specific to cchoir.

    Used for errors that should be catched by the CLI and shown to the user
    before quitting.
    """
