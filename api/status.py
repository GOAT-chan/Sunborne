from api.helper.base import get_status
from models.status import ServerStatus
from utils.logger import Logger

async def get_server_status() -> ServerStatus | None:
    r = await get_status()
    if not r:
        Logger.err("couldn't query server status, something is probably wrong")
        return None
    status = ServerStatus()
    status.maintenance = r['is_on_maintenance']
    status.online_users = r['users_online']
    status.total_users = r['total_users']
    status.scores_submitted = r['total_scores']
    return status