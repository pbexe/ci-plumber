import json
from pathlib import Path
from typing import Any

import typer


def get_config_file() -> Path:
    #
    """Gets the location of the config file, as well as ensuring it exists

    Returns:
        Path: The path to the config file
    """
    # Get the config directory
    app_dir: str = typer.get_app_dir("CI-Plumber")
    # Get the config file
    config_path: Path = Path(app_dir) / "config.json"
    # If it doesn't exist, create it
    if not config_path.is_file():
        typer.echo("Config file doesn't exist yet")
        # Make the config directory
        Path.mkdir(Path(app_dir), parents=True, exist_ok=True)
        # Make the config file
        config_path.touch()
        # Fill it with valid JSON
        with config_path.open("w") as fp:
            json.dump({"repos": {}}, fp)
        typer.echo("Created config file")
    return config_path


def load_config(
    config_path: Path, remote: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    #
    """Loads the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use

    Returns:
        tuple[dict[str, Any], dict[str, Any]]: The config and repo data
    """
    config: dict[str, Any] = {}
    with config_path.open("r") as fp:
        config = json.load(fp)
    current_config: dict[str, Any] = {}
    if remote in config["repos"]:
        current_config = config["repos"][remote]
    else:
        current_config = {}
    return current_config, config


def save_config(
    config_path: Path, remote: str, config: dict[str, Any]
) -> None:
    """Saves the config to the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use
        config (dict[str, Any]): The config to save
    """
    with config_path.open("w") as fp:
        json.dump(config, fp, indent=4)
