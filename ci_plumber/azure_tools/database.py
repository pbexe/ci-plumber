import json
import random
from enum import Enum
from pathlib import Path

import typer
from rich.console import Console

from ci_plumber.azure_tools.default_generators import (
    Locations,
    get_resource_group,
)
from ci_plumber.helpers import run_command


class DatabaseSku(str, Enum):
    """Enum for database sku types"""

    basic = "B_Gen5_1"
    general = "GP_Gen5_32"
    memory = "MO_Gen5_2"


class GeoRedundant(str, Enum):
    """Enum for geo redundant database"""

    disabled = "Disabled"
    enabled = "Enabled"


class SSL(str, Enum):
    """Enum for SSL"""

    disabled = "Disabled"
    enabled = "Enabled"


def create_database(
    name: str = typer.Option(
        "my-database-" + str(random.randint(100_000_000, 999_999_999)),
        help="Enter a unique name that identifies your Azure Database for "
        "MariaDB server. The server name can contain only lowercase letters, "
        "numbers, and the hyphen (-) character. It must contain between 3 and "
        "63 characters.",
        prompt=True,
    ),
    resource_group: str = get_resource_group(),
    sku: DatabaseSku = typer.Option(DatabaseSku.basic, help="Database SKU"),
    backup_retention: int = typer.Option(
        7, help="Database backup retention in days."
    ),
    geo_redundant: GeoRedundant = typer.Option(
        GeoRedundant.disabled,
        help="Whether geo-redundant backups should be enabled for this "
        "server.",
    ),
    location: Locations = typer.Option(
        Locations.uksouth, help="The Azure location for the server."
    ),
    ssl: SSL = typer.Option(
        SSL.enabled, help="Whether SSL should be enabled for this server."
    ),
    storage: int = typer.Option(
        51200,
        help="The storage capacity of the server (the unit is megabytes). "
        "Valid storage sizes are 5,120 MB (minimum) with increases in "
        "1,024-MB increments.",
    ),
    version: str = typer.Option("10.2", help="The version of MariaDB to use."),
    admin_username: str = typer.Option(
        "myadmin",
        help="The user name for the administrator login. The admin-user "
        "parameter can't be azure_superuser, admin, administrator, root, "
        "guest, or public.",
        prompt=True,
    ),
    admin_password: str = typer.Option(
        ...,
        help="The password of the administrator user. Your password must "
        "contain between 8 and 128 characters. It must contain characters "
        "from three of the following categories: English uppercase letters, "
        "English lowercase letters, numbers, and non-alphanumeric characters.",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
    ),
) -> None:
    """Create a database in Azure"""

    console = Console()

    with console.status(
        "[bold green]Creating the database...", spinner="clock"
    ):

        console.log("Initialising Server. [dim]This may take a while...[/dim]")
        # Create the database
        run_command(
            f"az mariadb server create "
            f"--resource-group {resource_group} "
            f"--name {name}  "
            f"--location {location} "
            f"--admin-user {admin_username} "
            f"--admin-password {admin_password} "
            f"--sku-name {sku} "
            f"--version {version} "
            f"--backup-retention {backup_retention} "
            f"--ssl-enforcement {ssl} "
            f"--storage-size {storage} "
            f"--geo-redundant-backup {geo_redundant} "
            "--only-show-errors"
        )

        # console.log(create)

        credentials_json = run_command(
            "az mariadb server show "
            f"--resource-group {resource_group} "
            f"--name {name}"
        )
        credentials = json.loads(credentials_json)

        console.log("Created Database")
        console.log("The credentials have been written to [bold]maria.env")
        console.log(credentials)

        # If there isn't a database config file, create one.
        db_config_file: Path = Path.cwd() / "maria.env"
        if not db_config_file.exists():
            db_config_file.touch()
            with db_config_file.open("w") as fp:
                fp.writelines(
                    [
                        f"ADMIN={credentials['adminstratorLogin']}\n"
                        f"ADMIN_PASSWORD={admin_password}\n"
                        f"HOST={credentials['fullyQualifiedDomainName']}\n"
                        f"NAME={name}\n"
                    ]
                )
        # TODO Check for duplication in the gitignore file.
        with (Path.cwd() / ".gitignore").open("a") as fp:
            fp.write("maria.env\n")
