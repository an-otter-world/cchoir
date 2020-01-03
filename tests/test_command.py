"""Command related unit tests."""
from cchoir.commands import configure
from cchoir.commands.deploy import DeployCommand

def test_deploy_arguments():
    """Check deploy command is correctly configured."""
    arguments = ['deploy']
    command, arguments = configure(arguments)
    assert isinstance(command, DeployCommand)
