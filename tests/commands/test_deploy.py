"""Command related unit tests."""
from cchoir.commands import configure
from cchoir.commands.deploy import DeployCommand


def test_deploy_arguments() -> None:
    """Check deploy command is correctly configured."""
    command, arguments = configure(['deploy'])
    assert isinstance(command, DeployCommand)
