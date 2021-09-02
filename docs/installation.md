## Requirements

- [Python 3.9+](https://www.python.org/downloads/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Openshift CLI](https://github.com/openshift/origin/releases/latest)
- Windows/Mac/Linux. Others may work but are untested.
- A supported project type. Currently supported:
    - Spring Boot
    - Flask
    - Or just a Dockerfile

## Installation


```console
// Install CI Plumber as well as all of the modules:
$ pip install ci-plumber[all]

// You can also install individual modules instead of the entire package:
$ pip install ci-plumber
$ pip install ci-plumber-azure

// Once installed, you can add tab completion:
$ ci-plumber --install-completion
```
