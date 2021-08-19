import json
from pathlib import Path
from typing import Any

import typer


def get_config_file() -> Path:
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
) -> tuple[dict[str, str], dict[str, dict[str, dict[str, str]]]]:
    """Loads the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use

    Returns:
        tuple[dict[str, str], dict[str, dict[str, dict[str, str]]]]: The config
            and repo data.
    """
    config: dict[str, dict[str, dict[str, str]]] = {}
    with config_path.open("r") as fp:
        config = json.load(fp)
    current_config: dict[str, str] = {}
    if remote in config["repos"]:
        current_config = config["repos"][remote]
    else:
        current_config = {}
    return current_config, config


def save_config(config_path: Path, config: dict[str, Any]) -> None:
    """Saves the config to the config file

    Args:
        config_path (Path): The path to the config file
        remote (str): The remote to use
        config (dict[str, Any]): The config to save
    """
    with config_path.open("w") as fp:
        json.dump(config, fp, indent=4)


def set_config(remote: str, key: str, value: Any) -> None:
    """Sets a config value"""
    config_path: Path = get_config_file()
    repo_config, config = load_config(config_path, remote)
    repo_config[key] = value
    config["repos"][remote] = repo_config
    save_config(config_path, config)


def get_config(remote: str, key: str) -> Any:
    """Gets a config value"""
    config_path: Path = get_config_file()
    repo_config, _ = load_config(config_path, remote)
    return repo_config[key]
