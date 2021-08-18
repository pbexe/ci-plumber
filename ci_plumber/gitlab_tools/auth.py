import gitlab

from ci_plumber.helpers import get_config_file, get_repo, load_config


def get_gitlab_client() -> gitlab.Gitlab:
    # Load the config
    current_config, _ = load_config(get_config_file(), get_repo())

    gitlab_url = current_config["gitlab_url"]
    access_token = current_config["access_token"]

    if "http" not in gitlab_url:
        gl = gitlab.Gitlab("https://" + gitlab_url, private_token=access_token)
    else:
        gl = gitlab.Gitlab(gitlab_url, private_token=access_token)

    return gl
