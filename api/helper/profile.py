import json

from httpx import AsyncClient
from utils.api import get_api_url
from utils.logger import Logger

client = AsyncClient()

async def get_profile(id: int) -> dict | None:
    r = await client.get(get_api_url(f"user/{id}"))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_profile failed for user {id} with code {r.status_code}")
        return None
    
async def get_profile_with_gamemode(id: int, gamemode: str) -> dict | None:
    r = await client.get(get_api_url(f"user/{id}/{gamemode}"))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_profile_with_gamemode failed for user {id} with code {r.status_code}")
        return None
    
async def get_profile_grades(id: int, gamemode: str) -> dict | None:
    r = await client.get(get_api_url(f"user/{id}/grades"),
                         params={"mode":gamemode})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_profile_grades failed for user {id} with code {r.status_code}")
        return None
    
async def get_profile_friends(id: int) -> dict | None:
    r = await client.get(get_api_url(f"user/{id}/friends/count"))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_profile_friends failed for user {id} with code {r.status_code}")
        return None
    
async def get_profile_medals(id: int, gamemode: str) -> dict | None:
    r = await client.get(get_api_url(f"user/{id}/medals"),
                         params={"mode":gamemode})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_profile_medals failed for user {id} with code {r.status_code}")
        return None
    
async def get_leaderboard(gamemode: str, count: int = 1, pages: int = 1, type: str = "Pp") -> dict | None:
    r = await client.get(get_api_url(f"user/leaderboard"),
                         params={"mode":gamemode,
                                 "limit":count,
                                 "page":pages,
                                 "type":type})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_leaderboard failed for user {id} with code {r.status_code}")
        return None