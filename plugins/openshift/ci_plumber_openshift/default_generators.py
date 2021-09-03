from typing import Any

import typer

from ci_plumber.helpers import get_config, get_repo


def get_gitlab_url() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "code_store.url"),
            help="The URL of the GitLab instance.",
        )
    except KeyError:
        return typer.Option(
            "git.cardiff.ac.uk",
            help="The URL of the GitLab instance.",
            prompt=True,
        )


def get_docker_registry_url() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "registry.url"),
            help="The URL of the Docker registry.",
        )
    except KeyError:
        return typer.Option(
            "registry.git.cf.ac.uk",
            help="The URL of the Docker registry.",
            prompt=True,
        )


def get_email() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "registry.email"),
            help="The email address to use.",
        )
    except KeyError:
        return typer.Option(
            ...,
            help="The email address to use.",
            prompt=True,
        )


def get_access_token() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "registry.password"),
            help="The access token to use.",
        )
    except KeyError:
        return typer.Option(
            ...,
            help="The access token to use.",
            prompt=True,
        )
