import json
from pathlib import Path
from typing import Any

import gitlab
import typer
from git import Repo
from git.remote import Remote
from git.util import IterableList

from ci_plumber.ci_yaml_template import template


def get_config_file() -> Path:
    """
    Gets the config file. Generates it if it doesn't exist.
    """
    # Get the config directory
    app_dir: str = typer.get_app_dir("CI-Plumber")
    # Get the config file
    config_path: Path = Path(app_dir) / "config.json"
    # If it doesn't exist, create it
    if not config_path.is_file():
        typer.echo("Config file doesn't exist yet")
        # Make the config directory
        Path.mkdir(Path(app_dir), parents=True, exist_ok=True)
        # Make the config file
        config_path.touch()
        # Fill it with valid JSON
        with config_path.open("w") as fp:
            json.dump({"repos": {}}, fp)
        typer.echo("Created config file")
    return config_path


def load_config(
    config_path: Path, remote: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Loads the config file
    """
    config: dict[str, Any] = {}
    with config_path.open("r") as fp:
        config = json.load(fp)
    current_config: dict[str, Any] = {}
    if remote in config["repos"]:
        current_config = config["repos"][remote]
    else:
        current_config = {}
    return current_config, config


def save_config(
    config_path: Path, remote: str, config: dict[str, Any]
) -> None:
    """
    Saves the config file
    """
    with config_path.open("w") as fp:
        json.dump(config, fp)


def generate_gitlab_yaml(yaml: Path) -> None:
    """
    Generates the .gitlab-ci.yml file if it doesn't exist
    """
    if not yaml.is_file():
        with yaml.open("w") as fp:
            fp.write(template)


def init(
    gitlab_url: str = typer.Option("https://git.cardiff.ac.uk", prompt=True),
    access_token: str = typer.Option(
        ...,
        prompt=True,
        help="GitLab access token. Please"
        " allow api, read_repository, and read_registry scopes.",
    ),
) -> None:
    """
    Initialise the project
    """
    typer.echo(typer.style("Initialising", dim=True))
    # Get the config file
    config_path: Path = get_config_file()
    # Get the repo
    repo: Repo = Repo(Path.cwd())
    # Check it isn't bare
    try:
        assert not repo.bare
    except AssertionError:
        typer.echo(
            "This directory is not a Git repository. Please run 'git init'"
            " first"
        )
        typer.Exit(1)
    # Get the remotes
    remotes: IterableList[Remote] = repo.remotes
    remote: str = ""
    if len(remotes) == 1:
        typer.echo("Found a remote")
        # Get the remote
        remote = remotes[0].url
    else:
        # TODO Allow for multiple remotes
        typer.echo("Found multiple/no remotes")
        typer.Exit(1)

    # Load the config
    current_config, config = load_config(config_path, remote)

    current_config["access_token"] = access_token

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

    # Generate .gitlab-ci.yml
    generate_gitlab_yaml(Path.cwd() / ".gitlab-ci.yml")

    # Save the config
    config["repos"][remote] = current_config
    save_config(config_path, remote, config)
