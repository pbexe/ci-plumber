import typer

from ci_plumber.init import init
from ci_plumber.openshift_wrapper import list_projects, openshift_deploy

app = typer.Typer()
app.command(name="init")(init)
app.command(name="openshift-deploy")(openshift_deploy)
app.command(name="list-projects")(list_projects)


@app.callback()
def callback() -> None:
    """
    CI Plumber
    """


if __name__ == "__main__":
    app()
