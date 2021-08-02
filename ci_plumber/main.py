import typer

app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    Awesome Portal Gun
    """


@app.command()
def shoot() -> None:
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load() -> None:
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
