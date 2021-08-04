import typer

from .init import init

app = typer.Typer()
app.command()(init)


@app.callback()
def callback() -> None:
    """
    CI Plumber
    """


if __name__ == "__main__":
    app()
