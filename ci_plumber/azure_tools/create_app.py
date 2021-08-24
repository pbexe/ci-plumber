import random
from time import sleep

import typer
from rich.console import Console

from ci_plumber.azure_tools.default_generators import (
    get_image,
    get_login_server,
    get_registry_name,
    get_resource_group,
)
from ci_plumber.helpers import run_command


def create_app(
    service_plan: str = typer.Option(
        "myServicePlan", help="Service plan name", prompt=True
    ),
    app_name: str = typer.Option(
        "myApp-" + str(random.randint(100_000_000, 999_999_999)),
        help="Application name",
        prompt=True,
    ),
    resource_group: str = get_resource_group(),
    os_type: str = typer.Option("linux", help="OS type"),
    image: str = get_image(),
    login_server: str = get_login_server(),
    registry_name: str = get_registry_name(),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbose output."
    ),
) -> None:
    """Creates an azure web app"""
    console = Console()
    with console.status(
        "[bold green]Creating the app...", spinner="clock"
    ) as _:
        # Create an App Service plan using the az appservice plan create
        # command
        console.log("Creating app service plan")
        service_plan_out = run_command(
            f"az appservice plan create --name {service_plan} --resource-group"
            f" {resource_group} --is-{os_type}"
        )
        if verbose:
            console.log(service_plan_out)

        registry = image

        # Create the web app with the az webpp create command
        console.log("Creating web app. [dim]This may take a while...[/dim]")
        create_app_out = run_command(
            f"az webapp create --resource-group {resource_group} --plan "
            f"{service_plan} --name {app_name} "
            f"--deployment-container-image-name {registry}"
        )
        if verbose:
            console.log(create_app_out)

        # Enable the system-assigned managed identity for the web app by using
        # the az webapp identity assign command
        console.log("Assigning managed identity")
        principal_id = run_command(
            f"az webapp identity assign --resource-group {resource_group} "
            f"--name {app_name} --query principalId --output tsv"
        ).rstrip()

        if verbose:
            console.log(principal_id)
        # console.log(f"Principal ID = {principal_id}")

        # Retrieve your subscription ID with the az account show command
        console.log("Retrieving subscription ID")
        subscription_id = run_command(
            "az account show --query id --output tsv"
        ).rstrip()

        if verbose:
            console.log(subscription_id)

        # Grant the managed identity permission to access the container
        # registry
        console.log("Granting permission to access container registry")

        sleep(5)  # It needs some time
        grant_out = run_command(
            f"az role assignment create --assignee {principal_id} --scope "
            f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
            f"/providers/Microsoft.ContainerRegistry/registries/"
            f"{registry_name} --role AcrPull"
        )

        if verbose:
            console.log(grant_out)

        # Configure your app to use the managed identity to pull from Azure
        # Container Registry
        console.log("Configuring app to use managed identity")
        configure_out = run_command(
            f"az resource update --ids /subscriptions/{subscription_id}/"
            f"resourceGroups/{resource_group}/providers/Microsoft.Web/sites/"
            f"{app_name}/config/web --set "
            "properties.acrUseManagedIdentityCreds=True"
        )

        if verbose:
            console.log(configure_out)

        # login_server = get_config(repo, "ACI_login_server")
        # Use the az webapp config container set command to specify the
        # container registry and the image to deploy for the web app
        console.log("Deploying")
        deploy_out = run_command(
            f"az webapp config container set --name {app_name} "
            f"--resource-group {resource_group} --docker-custom-image-name "
            f"{registry} --docker-registry-server-url https://{login_server}"
        )

        if verbose:
            console.log(deploy_out)

        console.log(
            f"Deployed to https://{app_name.lower()}.azurewebsites.net"
        )
        console.log("[dim]It may take a moment to come online")
