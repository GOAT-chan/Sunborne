import os
import json
from typing import Any
from loguru import logger

class Config:
    _path: str
    _data: dict
    def __init__(self, path: str):
        self._path = path
        self._ensure_config()
        self._load()
    def _ensure_config(self):
        if not os.path.isfile(self._path):
            logger.info(f"Generating new {self._path}...")
            with open(self._path, 'wt') as f:
                json.dump(self._get_template(), f, indent=4)
    def _load(self):
        with open(self._path, 'r') as f:
            self._data = json.load(f)
    def _get_template(self) -> dict:
        return {}
    def get_section(self, section: str) -> Any:
        keys = section.split(".")
        cursor = self._data.copy()
        for key in keys:
            cursor = cursor[key]
        return cursor
    @classmethod
    def load(cls, path: str):
        return cls(path)
    
app_config: Config = None
emoji_config: Config = None