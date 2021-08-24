import json
import subprocess

import typer
from rich.console import Console

from ci_plumber.helpers import run_command


def login() -> None:
    """Log in to Azure using Azure CLI."""
    subprocess.run("az login --use-device-code".split(), check=True)


def list_subscriptions() -> None:
    """List Azure subscriptions."""
    console = Console()
    accounts = json.loads(run_command("az account list"))

    for account in accounts:
        console.print(f"{account['name']}", end="", highlight=False)
        console.print(f" - {account['id']}", end="")
        console.print(" *" if account["isDefault"] else "")


def set_default_subscription(
    subscription_id: str = typer.Option(
        ...,
        help="The subscription ID to set as default.",
        prompt=True,
    )
) -> None:
    """Set default subscription."""
    run_command(f"az account set --subscription {subscription_id}")
