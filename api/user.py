from api.helper.profile import get_leaderboard, get_profile, get_profile_friends, get_profile_grades, get_profile_medals, get_profile_with_gamemode
from models.user import UserProfile
from utils.logger import Logger
from datetime import datetime
from cashews import cache, NOT_NONE

@cache(ttl="15m", condition=NOT_NONE)
async def get_complete_user_profile(id: int, gamemode: str = None) -> UserProfile | None:
    Logger.info(f"getting complete profile data for user id {id}")
    profile = UserProfile()
    basic_profile = await get_profile(id)
    if not basic_profile:
        Logger.err(f"couldn't find profile data for user id {id}")
        return None
    Logger.verbose(f"get_profile response: {basic_profile}")
    profile.user_name = basic_profile['username']
    profile.user_id = basic_profile['user_id']
    profile.country_code = basic_profile['country_code']
    profile.description = basic_profile['description']
    profile.avatar_url = basic_profile['avatar_url']
    profile.banner_url = basic_profile['banner_url']
    profile.registration_date = datetime.fromisoformat(basic_profile['register_date'])
    profile.last_online = datetime.fromisoformat(basic_profile['last_online_time'])
    profile.restricted = basic_profile['restricted']
    profile.badges = basic_profile['badges']
    profile.status = basic_profile['user_status']
    profile.default_gamemode = basic_profile['default_gamemode']
    friends = await get_profile_friends(id)
    Logger.verbose(f"get_profile_friends response: {friends}")
    profile.following = friends['following']
    profile.followers = friends['followers']
    if not gamemode:
        gamemode = profile.default_gamemode
    gamemode_profile = await get_profile_with_gamemode(id, gamemode)
    Logger.verbose(f"get_profile_with_gamemode response: {gamemode_profile}")
    profile.stats.gamemode = gamemode_profile['stats']['gamemode']
    profile.stats.global_rank = gamemode_profile['stats']['rank']
    profile.stats.country_rank = gamemode_profile['stats']['country_rank']
    profile.stats.play_count = gamemode_profile['stats']['play_count']
    profile.stats.play_time = gamemode_profile['stats']['play_time']
    profile.stats.total_score = gamemode_profile['stats']['total_score']
    profile.stats.ranked_score = gamemode_profile['stats']['ranked_score']
    profile.stats.accuracy = gamemode_profile['stats']['accuracy']
    profile.stats.total_pp = gamemode_profile['stats']['pp']
    profile.stats.max_combo = gamemode_profile['stats']['max_combo']
    profile.stats.peak_global_rank = gamemode_profile['stats']['best_global_rank']
    profile.stats.peak_country_rank = gamemode_profile['stats']['best_country_rank']
    profile.stats.peak_global_rank_date = datetime.fromisoformat(gamemode_profile['stats']['best_global_rank_date'])
    profile.stats.peak_country_rank_date = datetime.fromisoformat(gamemode_profile['stats']['best_country_rank_date'])
    grades = await get_profile_grades(id, gamemode)
    Logger.verbose(f"get_profile_grades response: {grades}")
    profile.stats.grades.rank_xh = grades['count_xh']
    profile.stats.grades.rank_x = grades['count_x']
    profile.stats.grades.rank_sh = grades['count_sh']
    profile.stats.grades.rank_s = grades['count_s']
    profile.stats.grades.rank_a = grades['count_a']
    medals = await get_profile_medals(id, gamemode)
    Logger.verbose(f"get_profile_medals response: {medals}")
    profile.stats.medals = len(medals['hush_hush']['medals']) + len(medals['beatmap_hunt']['medals']) + len(medals['mod_introduction']['medals']) + len(medals['skill']['medals'])
    return profile

@cache(ttl="15m")
async def get_top_players() -> list[UserProfile]:
    players = []
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
        # we get by pp, not total score (and who tf compares by score anyways)
        data = await get_leaderboard(m)
        Logger.verbose(f"raw leaderboard data: {data}")
        data = data['users'][0]
        # we just do this instead of calling get_complete_user_profile
        # it will be faster this way
        profile = UserProfile()
        profile.default_gamemode = m
        profile.user_name = data['user']['username']
        profile.user_id = data['user']['user_id']
        profile.registration_date = datetime.fromisoformat(data['user']['register_date'])
        profile.stats.total_pp = data['stats']['pp']
        profile.stats.accuracy = data['stats']['accuracy']
        profile.stats.play_count = data['stats']['play_count']
        players.append(profile)
    return players