import asyncio
import json
import os
from interactions import TYPE_ALL_CHANNEL
import websockets

from typing import Any
from utils.config import get_config
from utils.logger import Logger
from utils.messages import send_beatmap_status_change_message, send_new_score_message

async def recv_callback(data: Any, score_channel: TYPE_ALL_CHANNEL, beatmap_channel: TYPE_ALL_CHANNEL):
    data = json.loads(str(data))
    Logger.verbose(f"got raw websocket data: {data}")
    match(data['type']):
        case "NewScoreSubmitted":
            Logger.verbose("detected new score submission!")
            await send_new_score_message(score_channel, data['data'])
        case "CustomBeatmapStatusChanged":
            Logger.verbose("detected beatmap status change!")
            await send_beatmap_status_change_message(beatmap_channel, data['data'])
        case _:
            Logger.warn(f"received unhandled websocket event: {data['type']}")

async def handle_websocket(score_channel: TYPE_ALL_CHANNEL, beatmap_channel: TYPE_ALL_CHANNEL):
    Logger.info("initializing websocket connection...")
    while True:
        try:
            async with websockets.connect(f"wss://api.{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/ws",
                                          ping_interval=get_config().event_query_interval) as ws:
                async for msg in ws:
                    await recv_callback(msg, score_channel, beatmap_channel)
        except Exception as ex:
            Logger.err(f"websocket connection closed with error: {ex}, reconnecting...")
            await asyncio.sleep(get_config().event_query_interval)
            continue