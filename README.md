# Typer Template

## Installation
```sh
# Install dependencies
$ poetry install
$ poetry shell

# Install git hooks
$ pre-commit install
$ pre-commit autoupdate
$ pre-commit run --all-files
```

## Features

- Runs checks on commit
    - Flake8
    - Black
    - pre-commit-hooks checks
    - mypy
    - isort
- Installable as a script
