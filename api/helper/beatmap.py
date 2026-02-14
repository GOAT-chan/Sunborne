import json

from httpx import AsyncClient
from utils.api import get_api_url
from utils.logger import Logger
from cashews import cache, NOT_NONE

client = AsyncClient()

@cache(ttl="15m", condition=NOT_NONE)
async def get_beatmap(id: int) -> dict | None:
    r = await client.get(get_api_url(f"beatmap/{id}"))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_beatmap failed with code {r.status_code}")
        return None
    
@cache(ttl="15m", condition=NOT_NONE)
async def get_beatmap_pp(id: int) -> dict | None:
    r = await client.get(get_api_url(f"beatmap/{id}/pp"))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_beatmap_pp failed with code {r.status_code}")
        return None