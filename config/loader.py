from loguru import logger
from utils.environ import get_config_file_path, get_emoji_config_file_path
from config.scoped_configs import AppConfig, EmojiConfig
from config import config

class ConfigLoader:
    @staticmethod
    def load_all():
        config.app_config = AppConfig.load(get_config_file_path())
        config.emoji_config = EmojiConfig.load(get_emoji_config_file_path())