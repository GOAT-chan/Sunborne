from api.helper.beatmap import get_beatmap, get_beatmap_pp
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
    r_pp = await get_beatmap_pp(id)
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
            beatmap.stats.sr = r['star_rating_osu']
        # mania (+SV2)
        case 3 | 15:
            beatmap.stats.sr = r['star_rating_mania']
        # taiko (+RX/SV2)
        case 1 | 5 | 13:
            beatmap.stats.sr = r['star_rating_taiko']
        # ctb (+RX/SV2)
        case 2 | 6 | 14:
            beatmap.stats.sr = r['star_rating_ctb']
    beatmap.status = r['status']
    beatmap.stats.max_combo = r['max_combo']
    beatmap.stats.circle_count = r['count_circles']
    beatmap.stats.slider_count = r['count_sliders']
    beatmap.stats.spinner_count = r['count_spinners']
    beatmap.stats.ar = r['ar']
    beatmap.stats.cs = r['cs']
    beatmap.stats.drain = r['drain']
    beatmap.stats.od = r['accuracy']
    beatmap.stats.bpm = r['bpm']
    beatmap.stats.pp = r_pp['pp']
    try:
        beatmap.stats.pp_aim = r_pp['ppAim']
        beatmap.stats.pp_acc = r_pp['ppAccuracy']
        beatmap.stats.pp_speed = r_pp['ppSpeed']
    except KeyError as ex:
        Logger.verbose(f"couldn't get key {ex}, probably non-std gamemode")
        pass
    Logger.verbose(f"putting into cache...")
    put_to_cache(cache_key, beatmap)
    return beatmap