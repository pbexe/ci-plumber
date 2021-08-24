import typer

from ci_plumber.azure_tools.auth import (
    list_subscriptions,
    login,
    set_default_subscription,
)
from ci_plumber.azure_tools.create_app import create_app
from ci_plumber.azure_tools.create_registry import create_registry

app = typer.Typer()

app.command(name="create-registry")(create_registry)
app.command(name="login")(login)
app.command(name="create-app")(create_app)
app.command(name="set-default-subscription")(set_default_subscription)
app.command(name="list-subscriptions")(list_subscriptions)


@app.callback()
def callback() -> None:
    """
    Tools to manage deploying to Azure
    """


if __name__ == "__main__":
    app()
