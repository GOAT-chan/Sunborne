from api.helper.beatmap import get_beatmap
from models.beatmap import Beatmap
from utils.logger import Logger
from utils.cache import get_from_cache, put_to_cache
from datetime import datetime

async def get_beatmap_data(id: int) -> Beatmap | None:
    Logger.info(f"getting data for beatmap {id}")
    cache_key = f"%beatmap%{id}"
    if get_from_cache(cache_key):
        Logger.verbose("cache hit!")
        return get_from_cache(cache_key)
    r = await get_beatmap(id)
    Logger.verbose(f"raw beatmap data: {r}")
    beatmap = Beatmap()
    beatmap.set_id = r['beatmapset_id']
    beatmap.diff_id = id
    beatmap.title = r['title']
    beatmap.mapper = r['creator']
    beatmap.artist = r['artist']
    beatmap.diff = r['version']
    beatmap.length = r['hit_length']
    beatmap.mode_id = r['mode_int']
    beatmap.mode_name = r['mode']
    beatmap.last_updated = datetime.fromisoformat(r['last_updated'])
    match(beatmap.mode_id):
        # standard (+RX/AP/SV2)
        case 0 | 4 | 8 | 12:
            beatmap.sr = r['star_rating_osu']
        # mania (+SV2)
        case 3 | 15:
            beatmap.sr = r['star_rating_mania']
        # taiko (+RX/SV2)
        case 1 | 5 | 13:
            beatmap.sr = r['star_rating_taiko']
        # ctb (+RX/SV2)
        case 2 | 6 | 14:
            beatmap.sr = r['star_rating_ctb']
    beatmap.status = r['status']
    beatmap.max_combo = r['max_combo']
    beatmap.circle_count = r['count_circles']
    beatmap.slider_count = r['count_sliders']
    beatmap.spinner_count = r['count_spinners']
    beatmap.ar = r['ar']
    beatmap.cs = r['cs']
    beatmap.hp_drain = r['drain']
    beatmap.od = r['accuracy']
    beatmap.bpm = r['bpm']
    Logger.verbose(f"putting into cache...")
    put_to_cache(cache_key, beatmap)
    return beatmap