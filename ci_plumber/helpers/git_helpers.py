from pathlib import Path

import typer
from git import Repo
from git.remote import Remote
from git.util import IterableList


def get_repo(dir: Path = Path.cwd()) -> str:
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
        # typer.echo("Found a remote")
        # Get the remote
        remote = remotes[0].url
    else:
        # TODO Allow for multiple remotes
        raise KeyError("Found multiple/no remotes")
    return remote
