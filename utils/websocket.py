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
    await send_beatmap_status_change_message(beatmap_channel, {'beatmap': {'id': 4995778, 'beatmapset_id': 2329444, 'hash': '9a9e8e335df7388ad86e8e587c986505', 'version': 'Bullet Train', 'status': 'Loved', 'star_rating_osu': 10.3293, 'star_rating_taiko': 6.39689, 'star_rating_ctb': 8.28477, 'star_rating_mania': 3.89557, 'total_length': 120, 'max_combo': 1552, 'accuracy': 9.7, 'ar': 10, 'bpm': 265, 'convert': False, 'count_circles': 598, 'count_sliders': 400, 'count_spinners': 0, 'cs': 4.3, 'drain': 3.8, 'hit_length': 114, 'is_scoreable': True, 'is_ranked': False, 'last_updated': '2025-03-08T06:48:31.0000000+00:00', 'mode_int': 0, 'mode': 'Standard', 'ranked': 4, 'title': 'Mousou Chikan Express', 'artist': '7_7', 'creator': 'PixelX_', 'creator_id': 30553311, 'beatmap_nominator_user': {'user_id': 1004, 'username': 'Shinohara Yuu', 'description': None, 'country_code': 'JP', 'register_date': '2026-01-25T16:10:34.2237050+00:00', 'avatar_url': 'https://a.goatchan.duckdns.org/avatar/1004?1769357507772', 'banner_url': 'https://a.goatchan.duckdns.org/banner/1004?1769358154526', 'last_online_time': '2026-02-02T22:42:11.2821720+00:00', 'restricted': False, 'default_gamemode': 'Standard', 'badges': ['Admin', 'Bat'], 'user_status': 'Offline'}}, 'new_status': 'Loved', 'old_status': 'Graveyard', 'bat': {'user_id': 1004, 'username': 'Shinohara Yuu', 'description': None, 'country_code': 'JP', 'register_date': '2026-01-25T16:10:34.2237050+00:00', 'avatar_url': 'https://a.goatchan.duckdns.org/avatar/1004?1769357507772', 'banner_url': 'https://a.goatchan.duckdns.org/banner/1004?1769358154526', 'last_online_time': '2026-02-02T22:42:11.2821720+00:00', 'restricted': False, 'default_gamemode': 'Standard', 'badges': ['Admin', 'Bat'], 'user_status': 'Offline'}})
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