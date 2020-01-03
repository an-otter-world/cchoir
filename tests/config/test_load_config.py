"""Test config loading."""

from cchoir.config import load_config


def test_load_config(datadir):
    """Tests loading a default config works."""
    load_config(datadir / 'site.yaml')
