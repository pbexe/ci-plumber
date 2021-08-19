import subprocess
from pathlib import Path
from typing import Any

import gitlab
import typer
from kubernetes import config
from openshift.dynamic import DynamicClient

from ci_plumber.helpers import (
    get_config,
    get_config_file,
    get_repo,
    load_config,
)


def get_username() -> Any:
    try:
        return load_config(get_config_file(), get_repo(Path.cwd()))[0][
            "username"
        ]
    except KeyError:
        return ...


def openshift_deploy(
    project: str = typer.Option(..., help="Project name", prompt=True),
    username: str = typer.Option(
        get_username(), help="Openshift Username", prompt=True
    ),
    password: str = typer.Option(
        ...,
        help="Openshift Password",
        prompt=True,
        confirmation_prompt=True,
        hide_input=True,
    ),
) -> None:
    """Deploys a project to OpenShift"""

    # Load the config
    repo = get_repo(Path.cwd())
    gitlab_url = get_config(repo, "gitlab_url")
    # username = current_config["username"]
    docker_registry_url = get_config(repo, "docker_registry_url")
    email = get_config(repo, "email")
    access_token = get_config(repo, "access_token")

    if "http" not in gitlab_url:
        gl = gitlab.Gitlab("https://" + gitlab_url, private_token=access_token)
    else:
        gl = gitlab.Gitlab(gitlab_url, private_token=access_token)

    gl_project = gl.projects.get(get_config(repo, "gitlab_project_id"))

    # Login
    subprocess.run(
        ["oc", "login", "-u", username, "-p", password], check=True
    )  # nosec

    # Create a new project
    subprocess.run(["oc", "new-project", f"{project}"], check=True)  # nosec

    subprocess.run(
        [
            "oc",
            "create",
            "secret",
            "docker-registry",
            "gitlab",
            f"--docker-server={docker_registry_url}",
            f"--docker-username={username}",
            f"--docker-password={access_token}",
            f"--docker-email={email}",
        ],
        check=True,
    )  # nosec

    subprocess.run(
        ["oc", "secrets", "link", "builder", "gitlab", "--for=pull"],
        check=True,
    )  # nosec
    subprocess.run(
        ["oc", "secrets", "link", "default", "gitlab", "--for=pull"],
        check=True,
    )  # nosec
    subprocess.run(
        [
            "oc",
            "secrets",
            "link",
            "deployer",
            "gitlab",
            "--for=pull",
        ],
        check=True,
    )  # nosec

    subprocess.run(
        [
            "oc",
            "create",
            "secret",
            "docker-registry",
            "gitlab-delegated",
            f"--docker-server={gitlab_url}",
            f"--docker-username={username}",
            f"--docker-password={access_token}",
            f"--docker-email={email}",
        ],
        check=True,
    )  # nosec

    subprocess.run(
        ["oc", "secrets", "link", "builder", "gitlab-delegated", "--for=pull"],
        check=True,
    )  # nosec
    subprocess.run(
        ["oc", "secrets", "link", "default", "gitlab-delegated", "--for=pull"],
        check=True,
    )  # nosec
    subprocess.run(
        [
            "oc",
            "secrets",
            "link",
            "deployer",
            "gitlab-delegated",
            "--for=pull",
        ],
        check=True,
    )  # nosec

    subprocess.run(
        [
            "oc",
            "import-image",
            f"{gl_project.path}",
            f"--from={docker_registry_url}/{gl_project.path_with_namespace}",
            "--scheduled",
            "--confirm",
        ],
        check=True,
    )  # nosec

    subprocess.run(
        ["oc", "new-app", f"{gl_project.path}"], check=True
    )  # nosec
    subprocess.run(
        ["oc", "expose", f"svc/{gl_project.path}"], check=True
    )  # nosec
    subprocess.run(
        ["oc", "describe", f"routes/{gl_project.path}"], check=True
    )  # nosec


def list_projects() -> None:
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)

    v1_projects = dyn_client.resources.get(
        api_version="project.openshift.io/v1", kind="Project"
    )

    project_list = v1_projects.get()

    for project in project_list.items:
        typer.echo(f"{project.metadata.name}")


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


def create_database_command(
    config_path: Path = (Path.cwd() / "maria.env"),
) -> None:
    subprocess.run(
        [
            "oc",
            "new-app",
            "--template=openshift/mariadb-persistent",
            f"--param-file={config_path.resolve()}",
        ],
        check=True,
    )  # nosec
    subprocess.run(["oc", "expose", "service/mariadb"], check=True)  # nosec
    subprocess.run(["oc", "describe", "routes/mariadb"], check=True)  # nosec


def create_database() -> None:
    create_database_command()
