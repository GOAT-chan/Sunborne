import os
import sys
from loguru import logger
from constants import env_keys

def _get_env_name(key: str) -> str:
    return f"{env_keys.PREFIX}{key}"

def get_data_dir() -> str:
    return os.environ.get(_get_env_name(env_keys.DATA_DIRECTORY), "data")

def get_logs_dir() -> str:
    return os.path.join(get_data_dir(), "logs")

def get_config_file_path() -> str:
    return os.path.join(get_data_dir(), "config.json")

def get_emoji_config_file_path() -> str:
    return os.path.join(get_data_dir(), "emojis.json")

def get_database_file_path() -> str:
    return os.path.join(get_data_dir(), "database.db")

def get_bot_token() -> str:
    token = os.environ.get(_get_env_name(env_keys.BOT_TOKEN))
    if not token:
        logger.error(f"{_get_env_name(env_keys.BOT_TOKEN)} was not set, cannot continue.")
        sys.exit(1)
    return token

def get_server_domain() -> str:
    url = os.environ.get(_get_env_name(env_keys.SERVER_DOMAIN))
    if not url:
        logger.error(f"{_get_env_name(env_keys.SERVER_DOMAIN)} was not set, cannot continue.")
        sys.exit(1)
    return url