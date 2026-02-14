import asyncio
import os
import traceback

from cashews import cache
from api.status import get_server_status
from utils.logger import Logger
from utils.config import get_config, load_config
from database.manager import create_db
from interactions import BaseTrigger, Client, Intents, listen, Task, IntervalTrigger
from utils.messages import send_status_message
from utils.websocket import handle_websocket

bot = Client(intents=Intents.DEFAULT,
             send_command_tracebacks=False)

# we run it here so everything's ready to go
load_config()

@Task.create(IntervalTrigger(seconds=get_config().health_check_interval)) 
async def health_check():
    status = await get_server_status()
    if status:
        Logger.success("health check succeeded")
        Logger.verbose(f"{status.online_users}/{status.total_users} online, maintenance={status.maintenance}, score submitted: {status.scores_submitted}")
    else:
        Logger.err("health check failed")
    if get_config().channels.health_check:
        await send_status_message(bot.get_channel(get_config().channels.health_check), status)

@listen()
async def on_ready():
    if os.environ.get("SUNBORNE_DEBUG"):
        Logger.warn("debug logging is ENABLED, this might affect performance!")
    cache.setup("mem://")
    health_check.start()
    asyncio.create_task(handle_websocket(bot.get_channel(get_config().channels.score_submission), bot.get_channel(get_config().channels.beatmap_status)))
    if get_config().channels.health_check and not get_config().only_send_health_check_embed_when_failed:
        Logger.warn(f"bot will ALWAYS send server status messages regardless of queried status!")
        Logger.warn(f"to avoid unnecessary clutter, consider enabling \"only_send_health_check_embed_when_failed\"")
    Logger.info("Bot is now ready!")

if __name__ == '__main__':
    try:
        create_db()
        bot.load_extension("extensions.profile")
        bot.load_extension("extensions.top")
        bot.start(os.environ.get("SUNBORNE_DISCORD_BOT_TOKEN"))
    except Exception as ex:
        if "No token provided" in str(ex):
            Logger.err("please set \"SUNBORNE_DISCORD_BOT_TOKEN\"")
            exit(1)
        elif "An improper token" in str(ex):
            Logger.err("please re-check \"SUNBORNE_DISCORD_BOT_TOKEN\"")
            exit(1)
        elif "No such file or directory" in str(ex) and "config.json" in str(ex):
            Logger.err("please create a config file (config.json)")
            exit(1)
        else:
            Logger.err(traceback.format_exc())
            exit(1)