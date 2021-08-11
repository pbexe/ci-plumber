import json
from pathlib import Path
from typing import Any

import gitlab
import typer
from framework_detector import detect, get_dockerfile
from git import Repo
from git.remote import Remote
from git.util import IterableList

from ci_plumber.ci_yaml_template import template

# from git import remote


def get_config_file() -> Path:
    """Gets the location of the config file, as well as ensuring it exists

    Returns:
        Path: The path to the config file
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
    """Loads the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use

    Returns:
        tuple[dict[str, Any], dict[str, Any]]: The config and repo data
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
    """Saves the config to the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use
        config (dict[str, Any]): The config to save
    """
    with config_path.open("w") as fp:
        json.dump(config, fp, indent=4)


def generate_gitlab_yaml(yaml: Path, file_name: str = "gitlab-ci.yml") -> None:
    """Generates the GitLab CI YAML file if it doesn't exist

    Args:
        yaml (Path): The path to the directory to generate the YAML file in
        file_name (str, optional): The nameof the YAML file to generate.
                                   Defaults to "gitlab-ci.yml".
    """
    if not (yaml / file_name).is_file():
        with (yaml / file_name).open("w") as fp:
            fp.write(template)


def generate_docker_file(path: Path, file_name: str = "Dockerfile") -> None:
    """Gernerates the Dockerfile if it doesn't exist

    Args:
        path (Path): The path to the directory
        file_name (str, optional): The name of the dockerfile to generate.
                                   Defaults to "Dockerfile".
    """
    framework = detect(path)
    dockerfile = get_dockerfile(framework["dockerfile"])

    if not (path / file_name).is_file():
        with (path / file_name).open("w") as fp:
            fp.write(dockerfile)


def get_repo(dir: Path) -> str:
    """Gets a repo remote from a directory

    Args:
        dir (Path): The path to the directory to get the repo from

    Returns:
        str: The repo remote
    """
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
    return remote


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
    """Initialises the CI plumber

    Args:
        gitlab_url (str, optional): The URL of the GitLab instance to use.
            Defaults to typer.Option("git.cardiff.ac.uk", prompt=True).
        username (str, optional): The network username to use. Defaults to
            typer.Option( ..., prompt=True, help="Your network username" ).
        email (str, optional): The email address associated with that username.
            Defaults to typer.Option(..., prompt=True, help="Your network
            email").
        access_token (str, optional): The Gitlab access token to use. Defaults
            to typer.Option( ..., prompt=True, help="GitLab access token.
            Please allow api, read_repository, and " "read_registry scopes.").
        docker_registry_url (str, optional): The URL of the docker registry.
            Defaults to typer.Option( "registry.git.cf.ac.uk", prompt=True,
            help="The URL of the docker registry", ).
    """
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
