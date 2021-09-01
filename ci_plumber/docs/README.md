# Typer Template

[![CodeFactor](https://www.codefactor.io/repository/github/pbexe/ci-plumber/badge)](https://www.codefactor.io/repository/github/pbexe/ci-plumber) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ci-plumber) ![PyPI](https://img.shields.io/pypi/v/ci-plumber) ![PyPI - Downloads](https://img.shields.io/pypi/dm/ci-plumber) [![python-app](https://github.com/pbexe/ci-plumber/actions/workflows/python-app.yml/badge.svg)](https://github.com/pbexe/ci-plumber/actions/workflows/python-app.yml)

## Installation

```sh
pip install ci-plumber[all]
```

### Requirements

- `oc` CLI tool
- `az` CLI tool

## Usage

### GitLab
```sh
# Initialise the project
ci-plumber gitlab init
```

### OpenShift

```sh
# Deploy from the current docker registry to OpenShift
ci-plumber openshift deploy

# Create a new DB and store the credentials in maria.env
ci-plumber openshift create-db
```

### Azure

```sh
# Log in to Azure
ci-plumber azure login

# List your Azure subscriptions
ci-plumber azure list-subscriptions

# Set the subscription to use
ci-plumber azure set-default-subscription

# Create a docker registry
ci-plumber azure create-registry

# Trigger a build and push
git add .
git commit -m "Added Azure CI file"
git tag -a v1.0.0 -m "Version 1.0.0"
git push --follow-tags

# Deploy to Azure
ci-plumber azure create-app

# Create a database and store the credentials in maria.env
ci-plumber azure create-db
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
