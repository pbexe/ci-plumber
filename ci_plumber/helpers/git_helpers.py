from pathlib import Path
from typing import Union

# import typer
from git import InvalidGitRepositoryError, NoSuchPathError, Repo
from git.remote import Remote
from git.util import IterableList


def get_repo(git_dir: Path = Path.cwd()) -> str:
    """Gets a repo remote from a directory

    Args:
        dir (Path): The path to the directory to get the repo from

    Returns:
        str: The repo remote
    """
    # Get the repo
    remotes: Union[IterableList[Remote], None] = None
    try:
        repo: Repo = Repo(git_dir)
        assert not repo.bare
        remotes = repo.remotes
    except (InvalidGitRepositoryError, NoSuchPathError, AssertionError):
        # typer.echo(
        #     "This directory is not a Git repository. Please run 'git init'"
        #     " first"
        # )
        ...

    # Get the remote
    remote: str = ""
    if remotes and len(remotes) == 1:
        # Get the remote
        remote = remotes[0].url
    else:
        # TODO Allow for multiple remotes
        raise KeyError("Found multiple/no remotes")
    return remote
