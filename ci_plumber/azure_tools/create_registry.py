import json
import random
import subprocess

import gitlab
import typer
from rich.console import Console

from ci_plumber.gitlab_tools.auth import get_gitlab_client
from ci_plumber.helpers import generate_gitlab_yaml, get_repo, set_config
from ci_plumber.helpers.config_helpers import get_config


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
    console = Console()
    with console.status(
        "[bold green]Deploying the container registry...", spinner="clock"
    ) as _:
        console.log(f"Creating resource group {resource_group_name}")
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
        console.log(f"Creating registry {registry_name}")
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
        console.log("Enabling admin user")
        subprocess.run(
            f"az acr update -n {registry_name} --admin-enabled true".split(),
            check=True,
            capture_output=True,
            text=True,
        )

        # Get the admin's credentials
        console.log("Getting admin credentials")
        credentials_json = subprocess.run(
            f"az acr credential show --resource-group "
            f"{resource_group_name} --name {registry_name}".split(),
            check=True,
            capture_output=True,
            text=True,
        )

        # Down with JSON, long live the Python
        credentials = json.loads(credentials_json.stdout)

        repo = get_repo()

        console.log("Logging in to Gitlab")
        gl = get_gitlab_client()
        console.log("Gettingthe Gitlab project")
        gl_project = gl.projects.get(get_config(repo, "gitlab_project_id"))

        set_config(repo, "ACI_username", credentials["username"])
        set_config(repo, "ACI_password", credentials["passwords"][0]["value"])
        set_config(repo, "ACI_login_server", login_server)
        set_config(
            repo,
            "ACI_image",
            login_server + "/" + gl_project.path_with_namespace,
        )

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
        console.log("Creating .gitlab-ci.yml")
        generate_gitlab_yaml(
            file_name=".gitlab-ci.yml",
            overwrite=True,
            template="gitlab-ci-azure.yml",
        )
