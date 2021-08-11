import importlib.resources
from pathlib import Path

from framework_detector import detect, get_dockerfile

from ci_plumber import yaml_templates


def generate_gitlab_yaml(yaml: Path, file_name: str = "gitlab-ci.yml") -> None:
    """Generates the GitLab CI YAML file if it doesn't exist

    Args:
        yaml (Path): The path to the directory to generate the YAML file in
        file_name (str, optional): The nameof the YAML file to generate.
            Defaults to "gitlab-ci.yml".
    """
    if not (yaml / file_name).is_file():
        with (yaml / file_name).open("w") as fp:
            fp.write(
                importlib.resources.read_text(yaml_templates, "gitlab-ci.yml")
            )


def generate_docker_file(path: Path, file_name: str = "Dockerfile") -> None:
    """Gernerates the Dockerfile if it doesn't exist

    Args:
        path (Path): The path to the directory
        file_name (str, optional): The name of the dockerfile to generate.
            Defaults to "Dockerfile".
    """
    framework = detect(path)
    dockerfile = get_dockerfile(framework["dockerfile"])

    if not (path / file_name).is_file():
        with (path / file_name).open("w") as fp:
            fp.write(dockerfile)
