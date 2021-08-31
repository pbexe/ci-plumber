import json
import random
from enum import Enum

import gitlab
import typer
from rich.console import Console

from ci_plumber.azure_tools.default_generators import (
    Locations,
    get_resource_group,
)
from ci_plumber.gitlab_tools.auth import get_gitlab_client
from ci_plumber.helpers import (
    generate_gitlab_yaml,
    get_repo,
    run_command,
    set_config,
)
from ci_plumber.helpers.config_helpers import get_config


class Skus(str, Enum):
    """The available SKUs for Azure registries."""

    Basic = "Basic"
    Standard = "Standard"
    Premium = "Premium"


def create_registry(
    registry_name: str = typer.Option(
        "registry-" + str(random.randint(100_000_000, 999_999_999)),
        help="The name of the registry",
        prompt=True,
    ),
    resource_group_name: str = get_resource_group(),
    location: Locations = typer.Option(
        Locations.uksouth,
        help="The name of the location to create the registry in.",
    ),
    sku: Skus = typer.Option(Skus.Basic, help="The SKU of the registry."),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbose output."
    ),
) -> None:
    """Create a new Azure Container Registry"""
    # Create the resource group
    console = Console()
    with console.status(
        "[bold green]Deploying the container registry...", spinner="clock"
    ) as _:
        console.log(f"Creating resource group {resource_group_name}")
        run_command(
            f"az group create --name {resource_group_name} --location "
            f"{location}"
        )

        # Create the registry
        console.log(f"Creating registry {registry_name}")
        create_registry_json = run_command(
            f"az acr create --resource-group {resource_group_name} --name "
            f"{registry_name} --sku {sku}"
        )

        if verbose:
            console.log(create_registry_json)

        create_registry = json.loads(create_registry_json)

        login_server = create_registry["loginServer"]

        # Enable the admin user
        console.log("Enabling admin user")
        create_admin = run_command(
            f"az acr update -n {registry_name} --admin-enabled true"
        )

        if verbose:
            console.log(create_admin)

        # Get the admin's credentials
        console.log("Getting admin credentials")
        credentials_json = run_command(
            f"az acr credential show --resource-group "
            f"{resource_group_name} --name {registry_name}"
        )

        if verbose:
            console.log(credentials_json)

        # Down with JSON, long live the Python
        credentials = json.loads(credentials_json)

        repo = get_repo()

        if verbose:
            console.log(f"Repo: {repo}")

        console.log("Logging in to Gitlab")
        gl = get_gitlab_client()
        console.log("Gettingthe Gitlab project")
        gl_project = gl.projects.get(get_config(repo, "gitlab_project_id"))

        set_config(repo, "ACI_username", credentials["username"])
        set_config(repo, "ACI_password", credentials["passwords"][0]["value"])
        set_config(repo, "ACI_login_server", login_server)
        set_config(repo, "ACI_resource_group", resource_group_name)
        set_config(
            repo,
            "ACI_image",
            login_server + "/" + gl_project.path_with_namespace + ":latest",
        )
        set_config(repo, "ACI_registry_name", registry_name)

        console.log("Creating Azure access keys in Gitlab CI")
        try:
            gl_project.variables.create(
                {"key": "AZURE_REGISTRY", "value": login_server}
            )
            gl_project.variables.create(
                {"key": "AZURE_USERNAME", "value": credentials["username"]}
            )
            gl_project.variables.create(
                {
                    "key": "AZURE_PASSWORD",
                    "value": credentials["passwords"][0]["value"],
                }
            )
            gl_project.variables.create(
                {
                    "key": "AZURE_REGISTRY_IMAGE",
                    "value": login_server
                    + "/"
                    + gl_project.path_with_namespace,
                }
            )
        except gitlab.exceptions.GitlabCreateError:
            console.log(
                "Azure access keys already exist in Gitlab CI for "
                f"{gl_project.path_with_namespace}"
            )
            current_AZURE_REGISTRY = gl_project.variables.get("AZURE_REGISTRY")
            current_AZURE_REGISTRY.value = login_server
            current_AZURE_REGISTRY.save()

            current_AZURE_USERNAME = gl_project.variables.get("AZURE_USERNAME")
            current_AZURE_USERNAME.value = credentials["username"]
            current_AZURE_USERNAME.save()

            current_AZURE_PASSWORD = gl_project.variables.get("AZURE_PASSWORD")
            current_AZURE_PASSWORD.value = credentials["passwords"][0]["value"]
            current_AZURE_PASSWORD.save()

            current_AZURE_REGISTRY_IMAGE = gl_project.variables.get(
                "AZURE_REGISTRY_IMAGE"
            )
            current_AZURE_REGISTRY_IMAGE.value = (
                login_server + "/" + gl_project.path_with_namespace
            )
            current_AZURE_REGISTRY_IMAGE.save()

        console.log("Creating .gitlab-ci.yml")
        generate_gitlab_yaml(
            file_name=".gitlab-ci.yml",
            overwrite=True,
            template="gitlab-ci-azure.yml",
        )
