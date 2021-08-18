import json
import random
import subprocess

import typer

from ci_plumber.gitlab_tools.auth import get_gitlab_client
from ci_plumber.helpers import (
    generate_gitlab_yaml,
    get_config_file,
    get_repo,
    load_config,
)


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
    create_registry_json = subprocess.run(
        f"az acr create --resource-group {resource_group_name} --name "
        f"{registry_name} --sku {sku}".split(),
        check=True,
        capture_output=True,
        text=True,
    )

    create_registry = json.loads(create_registry_json.stdout)

    login_server = create_registry["loginServer"]

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

    gl = get_gitlab_client()
    current_config, _ = load_config(get_config_file(), get_repo())
    gl_project = gl.projects.get(current_config["gitlab_project_id"])
    gl_project.variables.create(
        {
            "AZURE_REGISTRY": login_server,
            "AZURE_USERNAME": credentials["username"],
            "AZURE_PASSWORD": credentials["passwords"][0]["value"],
            "AZURE_REGISTRY_IMAGE": login_server
            + gl_project.path_with_namespace,
        }
    )
    generate_gitlab_yaml(file_name="gitlab-ci-azure.yml", overwrite=True)
