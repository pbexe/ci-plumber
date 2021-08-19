import gitlab

from ci_plumber.helpers import get_config, get_repo


def get_gitlab_client() -> gitlab.Gitlab:
    # Load the config
    repo = get_repo()

    gitlab_url = get_config(repo, "gitlab_url")
    access_token = get_config(repo, "access_token")

    if "http" not in gitlab_url:
        gl = gitlab.Gitlab("https://" + gitlab_url, private_token=access_token)
    else:
        gl = gitlab.Gitlab(gitlab_url, private_token=access_token)

    return gl
