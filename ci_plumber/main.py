import importlib
import importlib.resources
import pkgutil

import typer
from rich.console import Console
from rich.markdown import Markdown

from ci_plumber import azure_tools, docs, gitlab_tools, openshift_tools

# https://packaging.python.org/guides/creating-and-discovering-plugins/
discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("ci_plumber_")
}


app = typer.Typer()
app.add_typer(openshift_tools.app, name="openshift")
app.add_typer(gitlab_tools.app, name="gitlab")
app.add_typer(azure_tools.app, name="azure")


for plugin in discovered_plugins:
    # We're going a bit ambiguous here with types so I've just turned mypy off
    try:
        app.add_typer(
            discovered_plugins[plugin].app,  # type: ignore
            name=discovered_plugins[plugin].name,  # type: ignore
        )
    except AttributeError:
        pass


@app.callback()
def callback() -> None:
    """
    CI Plumber
    """


@app.command()
def readme() -> None:
    """
    Show README.md
    """
    console = Console()
    readme = importlib.resources.read_text(docs, "README.md")
    console.print(Markdown(readme))


if __name__ == "__main__":
    app()
