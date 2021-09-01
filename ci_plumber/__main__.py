import click
import typer

from .main import app

# Allow ci-plumber to be called with `python -m ci_plumber`
try:
    app()
except click.exceptions.Exit:
    typer.Exit(1)
