import requests

APP_VERSION = "v1.1"

GITHUB_LATEST_RELEASE_URL = (
    "https://api.github.com/repos/Mohamed6886/COS_IOC-Blocking-Tool/releases/latest"
)

def check_for_update(timeout=3):
    """
    Returns (is_update_available, latest_version)
    Fails silently if GitHub is unreachable.
    """
    try:
        response = requests.get(GITHUB_LATEST_RELEASE_URL, timeout=timeout)
        response.raise_for_status()
        latest = response.json().get("tag_name")

        if latest and latest != APP_VERSION:
            return True, latest

    except Exception:
        pass

    return False, None