import typer

from ci_plumber import gitlab_tools, openshift_tools

app = typer.Typer()
app.add_typer(openshift_tools.app, name="openshift")
app.add_typer(gitlab_tools.app, name="gitlab")


@app.callback()
def callback() -> None:
    """
    CI Plumber
    """


if __name__ == "__main__":
    app()
