import json

from httpx import AsyncClient
from utils.api import get_api_url
from utils.logger import Logger

client = AsyncClient()

async def get_top_score(gamemode: str, count: int = 1, pages: int = 1) -> dict | None:
    r = await client.get(get_api_url("score/top"),
                         params={"mode":gamemode,
                                 "limit":count,
                                 "page":pages})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_top_score failed with code {r.status_code}")
        return None