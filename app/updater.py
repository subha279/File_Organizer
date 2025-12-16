import os
import sys

import requests
from packaging.version import Version

from .config import GITHUB_API_LATEST, VERSION


def check_update():
    r = requests.get(GITHUB_API_LATEST, timeout=5)
    data = r.json()

    latest_version = data["tag_name"].lstrip("v")
    if Version(latest_version) > Version(VERSION):
        asset = data["assets"][0]["browser_download_url"]
        return True, latest_version, asset

    return False, None, None


def apply_update(url):
    binary = sys.argv[0]
    new_file = binary + ".new"

    with requests.get(url, stream=True) as r:
        with open(new_file, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    os.replace(new_file, binary)
    os.execv(binary, sys.argv)
