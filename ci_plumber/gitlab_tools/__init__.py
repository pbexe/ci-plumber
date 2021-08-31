import typer

from ci_plumber import Module_attribute
from ci_plumber.gitlab_tools.init import init

attributes = [
    Module_attribute.source_code,
    Module_attribute.builder,
    Module_attribute.image_store,
]

name = "gitlab"

app: typer.Typer = typer.Typer()
app.command(name="init")(init)


@app.callback()
def callback() -> None:
    """
    Tools to manage Gitlab builds.
    """


if __name__ == "__main__":
    app()
