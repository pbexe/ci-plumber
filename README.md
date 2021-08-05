# Typer Template

## Installation

```sh
pip install ci-plumber --extra-index-url https://__token__:<your_personal_token>@git.cardiff.ac.uk/api/v4/projects/5484/packages/pypi/simple
```

## Usage

Initialise with a repo

```sh
ci-plumber init
```

## Developing

### Installation
```sh
# Install dependencies
$ poetry install
$ poetry shell

# Install git hooks
$ pre-commit install
$ pre-commit autoupdate
$ pre-commit run --all-files
```

### Features

- Runs checks on commit
    - Flake8
    - Black
    - pre-commit-hooks checks
    - mypy
    - isort
- Installable as a script
