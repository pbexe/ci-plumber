from enum import Enum
from typing import Any

import typer

from ci_plumber.helpers import get_config, get_repo


class Locations(str, Enum):
    """The available locations for Azure resources."""

    eastus = "eastus"
    eastus2 = "eastus2"
    southcentralus = "southcentralus"
    westus2 = "westus2"
    westus3 = "westus3"
    australiaeast = "australiaeast"
    southeastasia = "southeastasia"
    northeurope = "northeurope"
    swedencentral = "swedencentral"
    uksouth = "uksouth"
    westeurope = "westeurope"
    centralus = "centralus"
    northcentralus = "northcentralus"
    westus = "westus"
    southafricanorth = "southafricanorth"
    centralindia = "centralindia"
    eastasia = "eastasia"
    japaneast = "japaneast"
    jioindiawest = "jioindiawest"
    koreacentral = "koreacentral"
    canadacentral = "canadacentral"
    francecentral = "francecentral"
    germanywestcentral = "germanywestcentral"
    norwayeast = "norwayeast"
    switzerlandnorth = "switzerlandnorth"
    uaenorth = "uaenorth"
    brazilsouth = "brazilsouth"
    centralusstage = "centralusstage"
    eastusstage = "eastusstage"
    eastus2stage = "eastus2stage"
    northcentralusstage = "northcentralusstage"
    southcentralusstage = "southcentralusstage"
    westusstage = "westusstage"
    westus2stage = "westus2stage"
    asia = "asia"
    asiapacific = "asiapacific"
    australia = "australia"
    brazil = "brazil"
    canada = "canada"
    europe = "europe"
    india = "india"
    japan = "japan"
    uk = "uk"
    unitedstates = "unitedstates"
    eastasiastage = "eastasiastage"
    southeastasiastage = "southeastasiastage"
    centraluseuap = "centraluseuap"
    eastus2euap = "eastus2euap"
    westcentralus = "westcentralus"
    southafricawest = "southafricawest"
    australiacentral = "australiacentral"
    australiacentral2 = "australiacentral2"
    australiasoutheast = "australiasoutheast"
    japanwest = "japanwest"
    jioindiacentral = "jioindiacentral"
    koreasouth = "koreasouth"
    southindia = "southindia"
    westindia = "westindia"
    canadaeast = "canadaeast"
    francesouth = "francesouth"
    germanynorth = "germanynorth"
    norwaywest = "norwaywest"
    swedensouth = "swedensouth"
    switzerlandwest = "switzerlandwest"
    ukwest = "ukwest"
    uaecentral = "uaecentral"
    brazilsoutheast = "brazilsoutheast"
    qatarcentral = "qatarcentral"


def get_resource_group() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "ACI_resource_group"),
            help="The name of the resource group to use.",
            prompt=True,
        )
    except KeyError:
        return typer.Option(
            "myResourceGroup",
            help="The name of the resource group to use.",
            prompt=True,
        )


def get_image() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "ACI_image"), help="The name of the image to use."
        )
    except KeyError:
        return typer.Option(
            ...,
            help="The name of the image to use.",
            prompt=True,
        )


def get_login_server() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "ACI_login_server"),
            help="The name of the login server to use.",
        )
    except KeyError:
        return typer.Option(
            ...,
            help="The name of the login server to use.",
            prompt=True,
        )


def get_registry_name() -> Any:
    try:
        repo = get_repo()
        return typer.Option(
            get_config(repo, "ACI_registry_name"),
            help="The name of the registry to use.",
        )
    except KeyError:
        return typer.Option(
            ...,
            help="The name of the registry to use.",
            prompt=True,
        )
