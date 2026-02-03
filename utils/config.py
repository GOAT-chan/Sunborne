import json
import os

from utils.logger import Logger
from models.config import Config

config: Config

def load_config():
    global config
    data = json.load(open(os.path.join(os.getcwd(), "config.json")))
    config = Config.model_validate(data)
    if not os.path.isdir(os.path.join(os.getcwd(), "data")):
        os.mkdir(os.path.join(os.getcwd(), "data"))
    Logger.success("loaded config.json!")

def get_config() -> Config:
    return config