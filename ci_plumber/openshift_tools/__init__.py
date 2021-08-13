import typer

from ci_plumber.openshift_tools.openshift_wrapper import (
    create_database,
    create_db_config,
    list_projects,
    openshift_deploy,
)

app = typer.Typer()

app.command(name="openshift-deploy")(openshift_deploy)
app.command(name="list-projects")(list_projects)
app.command(name="create-database")(create_database)
app.command(name="create-db-config")(create_db_config)


@app.callback()
def callback() -> None:
    """
    Tools to manage deploying to Openshift
    """


if __name__ == "__main__":
    app()
