import json
import random
import subprocess

import typer


def create_registry(
    registry_name: str = typer.Option(
        str(random.randint(100_000_000, 999_999_999)),
        help="The name of the registry",
        prompt=True,
    ),
    resource_group_name: str = typer.Option(
        ...,
        help="The name of the resource group to create the registry in.",
        prompt=True,
    ),
    location: str = typer.Option(
        "uksouth",
        help="The name of the location to create the registry in.",
        prompt=True,
    ),
    sku: str = typer.Option("Basic", help="The SKU of the registry."),
) -> None:
    """Create a new Azure Container Registry"""

    # Create the resource group
    try:
        subprocess.run(
            f"az group create --name {resource_group_name} --location "
            f"{location}".split(),
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        # If the resource group already exists, ignore the error
        typer.echo("The resource group already exists")

    # Create the registry
    subprocess.run(
        f"az acr create --resource-group {resource_group_name} --name "
        f"{registry_name} --sku {sku}".split(),
        check=True,
        capture_output=True,
        text=True,
    )

    # Enable the admin user
    subprocess.run(
        f"az acr update -n {registry_name} --admin-enabled true".split(),
        check=True,
        capture_output=True,
        text=True,
    )

    # Get the admin's credentials
    credentials_json = subprocess.run(
        f"az acr credential show --resource-group "
        f"{resource_group_name} --name {registry_name}".split(),
        check=True,
        capture_output=True,
        text=True,
    )

    # Down with JSON, long live the Python
    credentials = json.loads(credentials_json.stdout)

    typer.echo(
        f"{credentials['username']}:"
        f"{credentials['passwords'][0]['value']}\nor\n"
        f"{credentials['passwords'][1]['value']}"
    )
    # TODO Load them into gitlab
