import sys
import niquests
from urllib.parse import urljoin
from loguru import logger
from constants import endpoints
from api.endpoints.user import BasicUser

class ServerAdapter:
    _session: niquests.AsyncSession
    api_url: str
    def __init__(self, url: str):
        self._session = niquests.AsyncSession()
        self.api_url = f"https://api.{url}"
    def _form_url(self, endpoint: str) -> str:
        return urljoin(self.api_url, endpoint)
    async def _get(self, endpoint: str, params: dict = {}) -> dict | str | None:
        logger.debug(f"Handling GET request: endpoint={endpoint},params={params}")
        r = await self._session.get(self._form_url(endpoint),
                                    params=params.copy())
        if r.status_code == 200:
            try:
                return r.json()
            except:
                return r.text
        logger.error(f"Request failed ({r.status_code}): endpoint={endpoint},params={params}")
        logger.error(f"Data: {r.text}")
        return None
    async def ping(self) -> bool:
        r = await self._get(endpoints.PING)
        if r:
            return True
        return False
    async def search_users(self, query: str, limit: int = 1) -> BasicUser | list[BasicUser] | None:
        r = await self._get(endpoints.SEARCH_USER,
                            params={
                                "query": query,
                                "limit": limit
                            })
        if not r or len(r) < 1:
            logger.error(f"search_users failed: query={query},limit={limit}")
            return None
        if limit > 1:
            users = []
            for i in r:
                users.append(BasicUser.from_response(i))
            return users
        return BasicUser.from_response(r[0])
    async def get_user(self, id: int) -> BasicUser | None:
        r = await self._get(endpoints.USER_INFO,
                            params={
                                "id": id
                            })
        if not r:
            logger.error(f"get_user failed: id={id}")
            return None
        return BasicUser.from_response(r)
    @classmethod
    async def init(cls, url: str):
        inst = cls(url)
        if not await inst.ping():
            logger.error(f"Server domain {url} doesn't seem to be reachable, cannot continue.")
            sys.exit(1)
        logger.success(f"Connected to {url}!")
        return inst
    
adapter: ServerAdapter = None