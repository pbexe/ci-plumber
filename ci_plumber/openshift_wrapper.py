import subprocess
from pathlib import Path

import gitlab
import typer
from kubernetes import config
from openshift.dynamic import DynamicClient

from ci_plumber.init import get_config_file, get_repo, load_config


def get_username() -> str:
    return load_config(get_config_file(), get_repo(Path.cwd()))[0]["username"]


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
    config_path: Path = get_config_file()
    current_config = load_config(config_path, get_repo(Path.cwd()))[0]
    gitlab_url = current_config["gitlab_url"]
    # username = current_config["username"]
    docker_registry_url = current_config["docker_registry_url"]
    email = current_config["email"]
    access_token = current_config["access_token"]

    if "http" not in gitlab_url:
        gl = gitlab.Gitlab("https://" + gitlab_url, private_token=access_token)
    else:
        gl = gitlab.Gitlab(gitlab_url, private_token=access_token)

    gl_project = gl.projects.get(current_config["gitlab_project_id"])

    # Login
    subprocess.run(["oc", "login", "-u", username, "-p", password], check=True)

    # Create a new project
    subprocess.run(["oc", "new-project", f"{project}"], check=True)

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
    )

    subprocess.run(
        ["oc", "secrets", "link", "builder", "gitlab", "--for=pull"],
        check=True,
    )
    subprocess.run(
        ["oc", "secrets", "link", "default", "gitlab", "--for=pull"],
        check=True,
    )
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
    )

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
    )

    subprocess.run(
        ["oc", "secrets", "link", "builder", "gitlab-delegated", "--for=pull"],
        check=True,
    )
    subprocess.run(
        ["oc", "secrets", "link", "default", "gitlab-delegated", "--for=pull"],
        check=True,
    )
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
    )

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
    )

    subprocess.run(["oc", "new-app", f"{gl_project.path}"], check=True)
    subprocess.run(["oc", "expose", f"svc/{gl_project.path}"], check=True)
    subprocess.run(["oc", "describe", f"routes/{gl_project.path}"], check=True)


def list_projects() -> None:
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)

    v1_projects = dyn_client.resources.get(
        api_version="project.openshift.io/v1", kind="Project"
    )

    project_list = v1_projects.get()

    for project in project_list.items:
        typer.echo(f"{project.metadata.name}")
