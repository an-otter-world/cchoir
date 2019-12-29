"""Command related unit tests."""
from caasa.commands import configure
from caasa.commands.deploy import DeployCommand

def test_deploy_arguments():
    """Check deploy command is correctly configured."""
    arguments = ['deploy']
    command, arguments = configure(arguments)
    assert isinstance(command, DeployCommand)
