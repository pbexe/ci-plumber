import importlib
import importlib.resources
import pkgutil

import typer
from rich.console import Console
from rich.markdown import Markdown

from ci_plumber import docs

# Get all of the modules that have the "ci_plumber_" prefix
# https://packaging.python.org/guides/creating-and-discovering-plugins/
discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("ci_plumber_")
}

# Create the main typer app
app = typer.Typer()

# For each of the plugins found, load them as sub-commands into the main app
for plugin in discovered_plugins:
    # We're going a bit ambiguous here with types so I've just turned mypy off
    try:
        app.add_typer(
            discovered_plugins[plugin].app,  # type: ignore
            name=discovered_plugins[plugin].name,  # type: ignore
        )
    except AttributeError:
        # It's always a possibility that there was a false positive plugin
        pass  # shhhh


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
