from utils.config import get_config

def map_sunrise_gamemode_to_sunborne(gamemode: str) -> str:
    match(gamemode):
        case "Standard":
            return "osu!"
        case "RelaxStandard":
            return "osu! (+RX)"
        case "AutopilotStandard":
            return "osu! (+AP)"
        case "ScoreV2Standard":
            return "osu! (+SV2)"
        case "Mania":
            return "osu!mania"
        case "ScoreV2Mania":
            return "osu!mania (+SV2)"
        case "Taiko":
            return "osu!taiko"
        case "RelaxTaiko":
            return "osu!taiko (+RX)"
        case "ScoreV2Taiko":
            return "osu!taiko (+SV2)"
        case "CatchTheBeat":
            return "osu!catch"
        case "RelaxCatchTheBeat":
            return "osu!catch (+RX)"
        case "ScoreV2CatchTheBeat":
            return "osu!catch (+SV2)"
        
def get_badges(badges: list[str]) -> str:
    config = get_config()
    badge = ""
    for b in badges:
        match(b):
            case "Admin":
                badge += config.emojis.admin_role + " "
            case "Bat":
                badge += config.emojis.bat_role + " "
            case "Developer":
                badge += config.emojis.dev_role + " "
    if badge != "":
        return badge
    else:
        return "None :/"

def get_ruleset_icon_url(gamemode: str) -> str:
    match(gamemode):
        case "Standard" | "RelaxStandard" | "AutopilotStandard" | "ScoreV2Standard":
            return "https://raw.githubusercontent.com/ppy/osu-resources/refs/heads/master/osu.Game.Resources/Textures/Icons/RulesetOsu.png"
        case "Mania" | "ScoreV2Standard":
            return "https://raw.githubusercontent.com/ppy/osu-resources/refs/heads/master/osu.Game.Resources/Textures/Icons/RulesetMania.png"
        case "Taiko" | "RelaxTaiko" | "ScoreV2Taiko":
            return "https://raw.githubusercontent.com/ppy/osu-resources/refs/heads/master/osu.Game.Resources/Textures/Icons/RulesetTaiko.png"
        case "CatchTheBeat" | "RelaxCatchTheBeat" | "ScoreV2CatchTheBeat":
            return "https://raw.githubusercontent.com/ppy/osu-resources/refs/heads/master/osu.Game.Resources/Textures/Icons/RulesetCatch.png"
        
def get_beatmap_cover_image_url(set_id: int, diff_id: int = None) -> str:
    url = f"https://assets.ppy.sh/beatmaps/{set_id}/covers/list.jpg"
    if diff_id:
        url += f"?{diff_id}"
    return url

def beatmap_status_name_to_emoji(name: str) -> str:
    match(name):
        case "Ranked":
            return get_config().emojis.ranked
        case "Approved":
            return get_config().emojis.approved
        case "Qualified":
            return get_config().emojis.qualified
        case "Loved":
            return get_config().emojis.loved
        case "Pending":
            return get_config().emojis.pending
        case "Wip":
            return get_config().emojis.wip
        case "Graveyard" | "Unknown":
            return get_config().emojis.graveyard

def grade_to_emoji(grade: str) -> str:
    match(grade):
        case "XH":
            return get_config().emojis.xh_rank
        case "X":
            return get_config().emojis.x_rank
        case "SH":
            return get_config().emojis.sh_rank
        case "S":
            return get_config().emojis.s_rank
        case "A":
            return get_config().emojis.a_rank
        case "B":
            return get_config().emojis.b_rank
        case "C":
            return get_config().emojis.c_rank
        case "D":
            return get_config().emojis.d_rank