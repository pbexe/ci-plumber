import typer
from ci_plumber_openshift.openshift_wrapper import (
    create_db,
    list_projects,
    openshift_deploy,
)

from ci_plumber import Module_attribute

attributes = [Module_attribute.consumer]

name = "openshift"

app: typer.Typer = typer.Typer()

app.command(name="deploy")(openshift_deploy)
app.command(name="ls")(list_projects)
app.command(name="create-db")(create_db)


@app.callback()
def callback() -> None:
    """
    Tools to manage deploying to Openshift
    """


if __name__ == "__main__":
    app()
