import os

from datetime import datetime
from interactions import TYPE_ALL_CHANNEL
from api.beatmap import get_beatmap_data
from api.user import get_complete_user_profile
from models.status import ServerStatus
from utils.config import get_config
from utils.embeds import EmbedBuilder
from utils.logger import Logger
from utils.misc import beatmap_status_name_to_emoji, get_beatmap_cover_image_url, get_ruleset_icon_url, grade_to_emoji, map_sunrise_gamemode_to_sunborne

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
        Logger.verbose(f"trying to send health check embed to channel {get_config().channels.health_check}")
        await channel.send(embed=embed.build())

async def send_new_score_message(channel: TYPE_ALL_CHANNEL, ws_data: dict):
    beatmap_data = await get_beatmap_data(ws_data['beatmap_id'])
    profile = await get_complete_user_profile(ws_data['user']['user_id'], beatmap_data.mode_name)
    embed = EmbedBuilder()
    embed.set_color(get_config().embed_colors.new_score)
    embed.set_header(f"{profile.user_name} (#{profile.stats.global_rank} - #{profile.stats.country_rank}{profile.country_code})", profile.avatar_url, f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/user/{profile.user_id}?mode={beatmap_data.mode_name}")
    embed.set_footer(f"{map_sunrise_gamemode_to_sunborne(profile.stats.gamemode)}", get_ruleset_icon_url(profile.stats.gamemode))
    embed.set_thumbnail_image(get_beatmap_cover_image_url(beatmap_data.set_id, beatmap_data.diff_id))
    embed.set_title(f"{beatmap_status_name_to_emoji(beatmap_data.status)} {beatmap_data.artist} - {beatmap_data.title} [{beatmap_data.diff}] ({round(beatmap_data.sr, 2)} {get_config().emojis.sr})", f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/beatmapsets/{beatmap_data.set_id}/{beatmap_data.diff_id}")
    embed.add_content(f"{grade_to_emoji(ws_data['grade'])} {str(ws_data['mods']).replace("None", "")} (<t:{round(datetime.fromisoformat(ws_data['when_played']).timestamp())}:R>)")
    embed.add_field("Score", f"{ws_data['total_score']:,}", True)
    embed.add_field("Accuracy", f"{round(ws_data['accuracy'], 2)}%", True)
    embed.add_field("pp", str(round(ws_data['performance_points'], 2)), True)
    embed.add_field("Combo", f"**x{ws_data['max_combo']}** / {beatmap_data.max_combo}", True)
    embed.add_field("Stats", f"{get_config().emojis.judge_300} {(ws_data['count_300'] + ws_data['count_geki'])} · {get_config().emojis.judge_100} {(ws_data['count_100'] + ws_data['count_katu'])} · {get_config().emojis.judge_50} {ws_data['count_50']} · {get_config().emojis.judge_miss} {ws_data['count_miss']}", True)
    Logger.verbose("sending new score submission embed")
    await channel.send(embed=embed.build())

async def send_beatmap_status_change_message(channel: TYPE_ALL_CHANNEL, ws_data: dict):
    pass