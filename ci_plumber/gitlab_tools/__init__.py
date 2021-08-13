import typer

from ci_plumber.gitlab_tools.init import init

app = typer.Typer()
app.command(name="init")(init)


@app.callback()
def callback() -> None:
    """
    Tools to manage Gitlab builds.
    """


if __name__ == "__main__":
    app()
