from pathlib import Path

import gitlab
import typer

from ci_plumber.config_helpers import get_config_file, load_config, save_config
from ci_plumber.file_generators import (
    generate_docker_file,
    generate_gitlab_yaml,
)
from ci_plumber.git_helpers import get_repo


def init(
    gitlab_url: str = typer.Option("git.cardiff.ac.uk", prompt=True),
    username: str = typer.Option(
        ..., prompt=True, help="Your network username"
    ),
    email: str = typer.Option(..., prompt=True, help="Your network email"),
    access_token: str = typer.Option(
        ...,
        prompt=True,
        help="GitLab access token. Please allow api, read_repository, and "
        "read_registry scopes.",
    ),
    docker_registry_url: str = typer.Option(
        "registry.git.cf.ac.uk",
        prompt=True,
        help="The URL of the docker registry",
    ),
) -> None:
    """Initialises the CI plumber"""
    typer.echo(typer.style("Initialising", dim=True))
    # Get the config file
    config_path: Path = get_config_file()
    remote = get_repo(Path.cwd())

    # Load the config
    current_config, config = load_config(config_path, remote)
    current_config["access_token"] = access_token

    if "http" not in gitlab_url:
        gl = gitlab.Gitlab("https://" + gitlab_url, private_token=access_token)
    else:
        gl = gitlab.Gitlab(gitlab_url, private_token=access_token)

    projects = gl.projects.list(owned=True)

    # Try to match the project with remote projects
    matches: bool = False
    for project in projects:
        if project.ssh_url_to_repo == remote:
            current_config["gitlab_project_id"] = project.id  # ssh matches
            matches = True
            break
        elif project.http_url_to_repo == remote:
            current_config["gitlab_project_id"] = project.id  # http matches
            matches = True
            break
    if not matches:
        typer.echo(f"{remote} doesn't match")
        typer.Exit(1)

    current_config["gitlab_url"] = gitlab_url
    current_config["username"] = username
    current_config["docker_registry_url"] = docker_registry_url
    current_config["email"] = email

    # Generate .gitlab-ci.yml
    generate_gitlab_yaml(Path.cwd(), "gitlab-ci.yml")
    generate_docker_file(Path.cwd(), "Dockerfile")

    # Save the config
    config["repos"][remote] = current_config
    save_config(config_path, remote, config)
