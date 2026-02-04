from interactions import TYPE_ALL_CHANNEL
from models.config import Channels
from models.status import ServerStatus
from utils.config import get_config
from utils.embeds import EmbedBuilder
from utils.logger import Logger
from datetime import datetime

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
        
async def send_status_message(channel: TYPE_ALL_CHANNEL, status: ServerStatus = None):
    embed = EmbedBuilder()
    embed.set_title("Server status check")
    embed.set_footer(f"Checked at {datetime.now().strftime("%H:%M %b %d, %Y")}")
    if not status:
        embed.set_color(get_config().embed_colors.error)
        embed.add_content("Server did not respond to status query. Something is probably (very) wrong.")
    else:
        embed.set_color(get_config().embed_colors.success)
        embed.add_content("Server responded to status query, everything's good!")
        embed.add_field("Online", f"**{status.online_users - 1}** / {status.total_users - 1}", True)
        embed.add_field("Score Submitted", str(status.scores_submitted), True)
        embed.add_field("Maintenance?", str(status.maintenance))
    if not status or status and not get_config().only_send_health_check_embed_when_failed:
        await channel.send(embed=embed.build())