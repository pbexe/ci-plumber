import typer

from ci_plumber.azure_tools.auth import login
from ci_plumber.azure_tools.create_app import create_app
from ci_plumber.azure_tools.create_registry import create_registry

app = typer.Typer()

app.command(name="create-registry")(create_registry)
app.command(name="login")(login)
app.command(name="create-app")(create_app)


@app.callback()
def callback() -> None:
    """
    Tools to manage deploying to Azure
    """


if __name__ == "__main__":
    app()
