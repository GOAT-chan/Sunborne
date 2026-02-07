from api.beatmap import get_beatmap_data
from api.helper.score import get_top_score
from api.user import get_complete_user_profile
from models.score import Score
from utils.cache import get_from_cache, put_to_cache
from utils.logger import Logger
from datetime import datetime

async def get_top_scores() -> list[Score]:
    cache_key = "%top_scores%"
    cached = get_from_cache(cache_key)
    if cached:
        Logger.verbose("cache hit!")
        return cached
    scores = []
    modes = [
            "Standard",
            "RelaxStandard",
            "AutopilotStandard",
            "ScoreV2Standard",
            "Mania",
            "ScoreV2Mania",
            "Taiko",
            "RelaxTaiko",
            "ScoreV2Taiko",
            "CatchTheBeat",
            "RelaxCatchTheBeat",
            "ScoreV2CatchTheBeat"
        ]
    for m in modes:
        Logger.verbose(f"(get_top_scores) fetching #1 score for gamemode {m}")
        r = await get_top_score(m)
        r = r['scores'][0]
        user = await get_complete_user_profile(r['user_id'])
        beatmap = await get_beatmap_data(r['beatmap_id'])
        score = Score()
        score.user = user
        score.beatmap = beatmap
        score.date = datetime.fromisoformat(r['when_played'])
        score.score_id = r['id']
        score.gamemode = m
        score.score = r['total_score']
        score.max_combo = r['max_combo']
        score.count_300 = r['count_300']
        score.count_100 = r['count_100']
        score.count_50 = r['count_50']
        score.count_miss = r['count_miss']
        score.accuracy = r['accuracy']
        score.pp = r['performance_points']
        score.mods = r['mods']
        score.grade = r['grade']
        scores.append(score)
    Logger.verbose("putting into cache")
    put_to_cache(cache_key, scores)
    return scores