import json

from httpx import AsyncClient
from utils.api import get_api_url
from utils.logger import Logger

client = AsyncClient()

async def get_status() -> dict | None:
    r = await client.get(get_api_url("status"),
                         params={"detailed":True})
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        Logger.err(f"get_status failed with code {r.status_code}")
        return None