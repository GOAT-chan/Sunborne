import os

from utils.logger import Logger

def get_api_url(endpoint: str) -> str:
    Logger.verbose(f"(get_api_url) constructed url: https://api.{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/{endpoint}")
    return f"https://api.{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/{endpoint}"