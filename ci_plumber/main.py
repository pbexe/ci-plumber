import importlib.resources

import typer
from rich.console import Console
from rich.markdown import Markdown

from ci_plumber import azure_tools, docs, gitlab_tools, openshift_tools

app = typer.Typer()
app.add_typer(openshift_tools.app, name="openshift")
app.add_typer(gitlab_tools.app, name="gitlab")
app.add_typer(azure_tools.app, name="azure")


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
