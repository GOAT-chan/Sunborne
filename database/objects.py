from dataclasses import dataclass
from datetime import datetime
from typing import Any
from sqlite3 import Row
from loguru import logger

@dataclass(init=False)
class UserLinkData:
    discord_id: int
    server_id: int
    link_date: datetime
    def to_sql(self) -> tuple[str, Any]:
        data = (self.discord_id, self.server_id, int(self.link_date.timestamp()))
        script = "INSERT INTO user_link VALUES(?, ?, ?)"
        return script, data
    @classmethod
    def from_sql_row(cls, data: Row):
        user = cls()
        user.discord_id = data[0]
        user.server_id = data[1]
        user.link_date = datetime.fromtimestamp(data[2])
        return user
    @classmethod
    def new(cls, discord_id: int, server_id: int):
        user = cls()
        user.discord_id = discord_id
        user.server_id = server_id
        user.link_date = datetime.now()
        return user
    
@dataclass(init=False)
class UserPreferencesData:
    discord_id: int
    last_changed_date: datetime
    def to_sql(self) -> tuple[str, Any]:
        data = (self.discord_id, int(self.last_changed_date.timestamp()))
        script = "INSERT INTO user_preferences VALUES(?, ?)"
        return script, data
    @classmethod
    def from_sql_row(cls, data: Row):
        pref = cls()
        pref.discord_id = data[0]
        pref.last_changed_date = datetime.fromtimestamp(data[1])
        return pref
    @classmethod
    def new(cls, discord_id: int):
        pref = cls()
        pref.discord_id = discord_id
        pref.last_changed_date = datetime.now()
        return pref