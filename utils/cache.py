from utils.logger import Logger
from typing import Any
from cacheout import Cache

cache = Cache(ttl=120)

def get_cache_key(identifier: str) -> str:
    return f"CACHE:{identifier}"

def put_to_cache(identifier: str, content: Any):
    key = get_cache_key(identifier)
    Logger.verbose(f"adding {key} to cache...")
    cache.add(key, content)
    
def get_from_cache(identifier: str) -> Any:
    key = get_cache_key(identifier)
    Logger.verbose(f"trying to retrieve {key} from cache...")
    return cache.get(key)

def remove_from_cache(identifier: str):
    key = get_cache_key(identifier)
    Logger.verbose(f"removing {key} from cache...")
    cache.delete(key)