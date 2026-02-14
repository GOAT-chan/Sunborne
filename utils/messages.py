import os

from datetime import datetime
from interactions import TYPE_ALL_CHANNEL, Button, ButtonStyle, GuildForum
from api.beatmap import get_beatmap_data
from api.user import get_complete_user_profile
from models.status import ServerStatus
from utils.cache import get_from_cache, put_to_cache, remove_from_cache
from utils.config import get_config
from utils.embeds import EmbedBuilder
from utils.logger import Logger
from utils.misc import beatmap_status_name_to_emoji, get_beatmap_cover_image_url, get_gamemode_tag_from_config, get_ranking_status_tag_from_config, get_ruleset_icon_url, grade_to_emoji, map_sunrise_gamemode_to_sunborne

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
    embed.set_title(f"{beatmap_status_name_to_emoji(beatmap_data.status)} {beatmap_data.artist} - {beatmap_data.title} [{beatmap_data.diff}] ({round(beatmap_data.stats.sr, 2)} {get_config().emojis.sr})", f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/beatmapsets/{beatmap_data.set_id}/{beatmap_data.diff_id}")
    embed.add_content(f"{grade_to_emoji(ws_data['grade'])} {str(ws_data['mods']).replace("None", "")} (<t:{round(datetime.fromisoformat(ws_data['when_played']).timestamp())}:R>)")
    embed.add_field("Score", f"{ws_data['total_score']:,}", True)
    embed.add_field("Accuracy", f"{round(ws_data['accuracy'], 2)}%", True)
    embed.add_field("pp", str(round(ws_data['performance_points'])), True)
    embed.add_field("Combo", f"**x{ws_data['max_combo']}** / {beatmap_data.stats.max_combo}", True)
    embed.add_field("Stats", f"{get_config().emojis.judge_300} {ws_data['count_300']} · {get_config().emojis.judge_100} {ws_data['count_100']} · {get_config().emojis.judge_50} {ws_data['count_50']} · {get_config().emojis.judge_miss} {ws_data['count_miss']}", True)
    Logger.verbose("sending new score submission embed")
    score_button = Button(
        style=ButtonStyle.URL,
        label="View score",
        url=f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/score/{ws_data['id']}"
    )
    await channel.send(embed=embed.build(), components=[score_button])

async def send_beatmap_status_change_message(channel: GuildForum, ws_data: dict):
    beatmap_data = await get_beatmap_data(ws_data['beatmap']['id'])
    profile = await get_complete_user_profile(ws_data['bat']['user_id'])

    post_name = f"{beatmap_data.artist} - {beatmap_data.title} ({beatmap_data.set_id})"

    posts = channel.get_posts()

    # try to find existing post
    post = next((p for p in posts if p.name == post_name), None)

    if not post:
        Logger.verbose(f"no post for beatmap set {beatmap_data.set_id} exist yet, creating new one")
        info_embed = EmbedBuilder()
        info_embed.set_color(get_config().embed_colors.beatmap_status_change)
        info_embed.set_title("Beatmap ranking status change")
        info_embed.set_header(profile.user_name, profile.avatar_url, f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/user/{profile.user_id}")
        info_embed.set_footer(f"{map_sunrise_gamemode_to_sunborne(beatmap_data.mode_name)}", get_ruleset_icon_url(beatmap_data.mode_name))
        info_embed.set_thumbnail_image(get_beatmap_cover_image_url(beatmap_data.set_id))
        info_embed.add_field("Mapper", beatmap_data.mapper, True)
        info_embed.add_field("Length", f"{datetime.fromtimestamp(beatmap_data.length).strftime("%M:%S")}", True)
        info_embed.add_field("Ranking", f"{beatmap_status_name_to_emoji(ws_data['old_status'])} **{ws_data['old_status']}**  >>  {beatmap_status_name_to_emoji(ws_data['new_status'])} **{ws_data['new_status']}**", True)
        beatmap_button = Button(style=ButtonStyle.URL,
                                label="View beatmap",
                                url=f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/beatmapsets/{beatmap_data.set_id}")
        post = await channel.create_post(name=post_name,
                                         content="",
                                         applied_tags=[
                                            channel.get_tag(get_gamemode_tag_from_config(beatmap_data.mode_name)),
                                            channel.get_tag(get_ranking_status_tag_from_config(ws_data['new_status']))
                                         ],
                                         components=[beatmap_button],
                                         embed=info_embed.build())

    # get the initial "post" message
    # post.initial_post is unreliable, so we do this cursed workaround
    initial_post = await post.fetch_messages(1)
    initial_post = initial_post[0]

    # construct from it
    new_embed = EmbedBuilder()
    new_embed.construct_from(initial_post.embeds[0])

    # append new diff data
    new_embed.add_content(f"\n[**{round(beatmap_data.stats.sr, 2)}** {get_config().emojis.sr}] **{beatmap_data.diff}**", False)
    new_embed.add_content(f"\n{get_config().emojis.cs} {str(beatmap_data.stats.cs)} {get_config().emojis.ar} {str(beatmap_data.stats.ar)} {get_config().emojis.od} {str(beatmap_data.stats.od)} {get_config().emojis.hp} {str(beatmap_data.stats.drain)} {get_config().emojis.bpm} {str(beatmap_data.stats.bpm)}", False)
    new_embed.add_content(f"\npp for {get_config().emojis.x_rank}: {round(beatmap_data.stats.pp)}\n")

    # update original message
    await initial_post.edit(embed=new_embed.build())
