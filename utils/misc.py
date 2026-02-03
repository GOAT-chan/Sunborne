# fun fact: i ion need to do ts
# but i dont like sunrise's gamemode names lol
from utils.config import get_config
from utils.logger import Logger


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