import typer

from ci_plumber import Module_attribute

attributes = [
    Module_attribute.source_code,
    Module_attribute.builder,
    Module_attribute.image_store,
    Module_attribute.consumer,
]

name = "example"
app: typer.Typer = typer.Typer()


@app.callback()
def callback() -> None:
    """
    This is an example of how to structure ci-plumber modules.
    """
