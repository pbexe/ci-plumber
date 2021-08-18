import subprocess


def login() -> None:
    """Log in to Azure using Azure CLI."""
    subprocess.run("az login --use-device-code".split(), check=True)
