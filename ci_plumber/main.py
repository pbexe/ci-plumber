from pathlib import Path

import typer
from git import Repo

app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    CI Plumber
    """


@app.command()
def init() -> None:
    """
    Initialise the project
    """
    typer.echo("Initialising app")

    # Get the config directory
    app_dir: str = typer.get_app_dir("CI-Plumber")
    # Get the config file
    config_path: Path = Path(app_dir) / "config.json"
    # If it doesn't exist, create it
    if not config_path.is_file():
        typer.echo("Config file doesn't exist yet")
        Path.mkdir(Path(app_dir), parents=True, exist_ok=True)
        config_path.touch()
        typer.echo("Created config file")
    # Get the repo
    repo = Repo(Path.cwd())
    # Check it isn't bare
    assert not repo.bare
    # Get the remotes
    remotes = repo.remotes

    if len(remotes) == 1:
        typer.echo("Found a remote")
        # Get the remote
        remote: str = remotes[0].url
        remote
    else:
        # TODO Allow for multiple remotes
        typer.echo("Found multiple remotes")
        typer.Exit(1)


@app.command()
def pwd() -> None:
    typer.echo(Path.cwd())


if __name__ == "__main__":
    app()
