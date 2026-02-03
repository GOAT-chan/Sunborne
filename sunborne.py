import os
import traceback

from utils.logger import Logger
from utils.config import load_config
from database.manager import create_db
from interactions import Client, Intents, listen

bot = Client(intents=Intents.DEFAULT)

@listen()
async def on_ready():
    Logger.success("Bot is now ready!")

if __name__ == '__main__':
    try:
        load_config()
        create_db()
        bot.load_extension("extensions.profile")
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