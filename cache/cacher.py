from cashews import cache
from constants.cache_keys import PROFILE_LINKING_DATA

async def set_profile_linking_data(discord_id: int, server_id: int):
    await cache.set(key=f"{PROFILE_LINKING_DATA}{discord_id}",
                    value=server_id,
                    expire="2m")
    
async def get_profile_linking_data(discord_id: int) -> int | None:
    return await cache.get(f"{PROFILE_LINKING_DATA}{discord_id}")