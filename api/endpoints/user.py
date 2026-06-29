from dataclasses import dataclass
from datetime import datetime
from utils.time import from_iso8601
from constants.gamemode import Gamemode

@dataclass(init=False)
class BasicUser:
    name: str
    id: str
    country: str
    description: str
    registered_date: datetime
    default_gamemode: Gamemode
    avatar_url: str
    banner_url: str
    @classmethod
    def from_response(cls, response: dict):
        user = cls()
        user.name = response['username']
        user.id = response['user_id']
        user.country = response['country_code']
        user.description = response['description']
        user.registered_date = from_iso8601(response['register_date'])
        user.default_gamemode = Gamemode[response['default_gamemode']]
        user.avatar_url = response['avatar_url']
        user.banner_url = response['banner_url']
        return user