from pathlib import Path

import typer
from rich.console import Console

from ci_plumber.helpers import (
    generate_docker_file,
    generate_gitlab_yaml,
    get_repo,
)
from ci_plumber.helpers.config_helpers import set_config
from ci_plumber_gitlab.auth import get_gitlab_client


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
    """Initialises Gitlab: Logs in and determines the gitlab repo to use."""
    console = Console()
    with console.status(
        "[bold green]Configuring Gitlab...", spinner="clock"
    ) as _:
        console.print("Getting remote")
        remote = get_repo(Path.cwd())
        set_config(remote, "gitlab_url", gitlab_url)
        set_config(remote, "username", username)
        set_config(remote, "docker_registry_url", docker_registry_url)
        set_config(remote, "email", email)
        set_config(remote, "access_token", access_token)

        console.log("Logging in to Gitlab")
        gl = get_gitlab_client()
        console.log("Getting projects")
        projects = gl.projects.list(owned=True)

        console.log("Matching remote with Gitlab projects")
        # Try to match the project with remote projects
        matches: bool = False
        for project in projects:
            if project.ssh_url_to_repo == remote:
                set_config(remote, "gitlab_project_id", project.id)
                matches = True
                console.log("Found project: {}".format(project.name))
                break
            elif project.http_url_to_repo == remote:
                set_config(remote, "gitlab_project_id", project.id)
                matches = True
                console.log("Found project: {}".format(project.name))
                break
        if not matches:
            console.log(f"[bold red]{remote} doesn't match")
            typer.Exit(1)

        # Generate .gitlab-ci.yml
        console.log("Generating .gitlab-ci.yml")
        generate_gitlab_yaml(Path.cwd(), "gitlab-ci.yml")
        console.log("Generating Dockerfile")
        generate_docker_file(Path.cwd(), "Dockerfile")

        console.log("[bold green]Gitlab configured!")
