import sys
import os
import asyncio
from cashews import cache
from loguru import logger
from dotenv import load_dotenv
from interactions import Client, Intents, listen
from interactions.api.events.internal import Startup
from utils.environ import get_data_dir, get_logs_dir, get_bot_token, get_server_domain
from utils.time import get_current_time, TimeFormat
from api import adapter
from config.loader import ConfigLoader
from database import manager as db

bot = Client(intents=Intents.DEFAULT,
             send_command_tracebacks=False)

@listen(Startup)
async def on_ready():
    logger.success("Bot is ready to go!")

def init_logger():
    logger.remove()
    logger.add(os.path.join(get_logs_dir(), 
               f"{get_current_time(TimeFormat.LOG_FILE_TIMESTAMP)}.log"),
               format="[{time:HH:mm:ss}] {level}: {message}",
               rotation="12:00")
    logger.add(sys.stdout,
               colorize=True,
               format="<fg #3e6b6a>[{time:HH:mm:ss}]</fg #3e6b6a> <level>{level}</level>: {message}")
    logger.level("INFO",
                 color="<fg #4388a8>")
    logger.level("SUCCESS",
                 color="<fg #3ab073>")
    logger.level("WARNING",
                 color="<fg #a9b046>")
    logger.level("ERROR",
                 color="<fg #b05446>")
    logger.level("DEBUG",
                 color="<fg #5438a1>")

def init():
    load_dotenv()
    os.makedirs(get_data_dir(), exist_ok=True)
    os.makedirs(get_logs_dir(), exist_ok=True)
    init_logger()
    logger.info("Initializing cache...")
    cache.setup("mem://")
    logger.info("Loading configuration files...")
    ConfigLoader.load_all()
    logger.info("Loading database...")
    db.database = asyncio.run(db.Database.init())
    logger.info("Setting up server adapter...")
    adapter.adapter = asyncio.run(adapter.ServerAdapter.init(get_server_domain()))
    logger.info("Starting up bot...")
    bot.load_extensions("commands")
    bot.start(get_bot_token())

if __name__ == "__main__":
    init()
