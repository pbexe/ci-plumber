from pathlib import Path

import typer


def create_db_config(
    memory_limit: str = typer.Option(
        "512Mi", help="Maximum amount of memory the container can use."
    ),
    namespace: str = typer.Option(
        "openshift",
        help="The OpenShift Namespace where the ImageStream resides.",
    ),
    database_service_name: str = typer.Option(
        "mariadb", help="Database service name"
    ),
    mysql_user: str = typer.Option(
        "maria_user",
        help="Username for MariaDB user that will be used for accessing the "
        "database.",
    ),
    mysql_password: str = typer.Option(
        ...,
        help="Password for the MariaDB connection user.",
        prompt=True,
        hide_input=True,
    ),
    mysql_root_password: str = typer.Option(
        ...,
        help="Password for the MariaDB root user.",
        prompt=True,
        hide_input=True,
    ),
    mysql_database: str = typer.Option(
        "sampledb", help="Name of the MariaDB database accessed."
    ),
    mariadb_version: str = typer.Option(
        "10.2",
        help="Version of MariaDB image to be used (10.1, 10.2 or latest).",
    ),
    volume_capacity: str = typer.Option(
        "1Gi", help="Volume space available for data, e.g. 512Mi, 2Gi."
    ),
) -> None:
    # If there isn't a database config file, create one.
    db_config_file: Path = Path.cwd() / "maria.env"
    if not db_config_file.exists():
        db_config_file.touch()
        with db_config_file.open("w") as fp:
            fp.writelines(
                [
                    f"MEMORY_LIMIT={memory_limit}\n",
                    f"NAMESPACE={namespace}\n",
                    f"DATABASE_SERVICE_NAME={database_service_name}\n",
                    f"MYSQL_USER={mysql_user}\n",
                    f"MYSQL_PASSWORD={mysql_password}\n",
                    f"MYSQL_ROOT_PASSWORD={mysql_root_password}\n",
                    f"MYSQL_DATABASE={mysql_database}\n",
                    f"MARIADB_VERSION={mariadb_version}\n",
                    f"VOLUME_CAPACITY={volume_capacity}\n",
                ]
            )
    # TODO Check for duplication in the gitignore file.
    with (Path.cwd() / ".gitignore").open("a") as fp:
        fp.write("maria.env\n")
