import os

from api.score import get_recent_score
from api.user import get_complete_user_profile
from database.manager import DbSession
from database.models.user import User
from models.user import UserProfile
from utils.logger import Logger
from utils.embeds import EmbedBuilder
from utils.config import get_config
from utils.db import check_if_user_id_is_claimed, find_linked_profile
from utils.misc import beatmap_status_name_to_emoji, get_badges, get_beatmap_cover_image_url, get_ruleset_icon_url, grade_to_emoji, map_sunrise_gamemode_to_sunborne
from interactions import Extension, SlashContext, OptionType, Member, SlashCommandChoice, slash_command, slash_option
from datetime import datetime

class ScoreExtension(Extension):
    @slash_command(name="rs",
                   description="Get your or someone's most recent score")
    @slash_option(name="user_id",
                  description="User ID",
                  required=False,
                  opt_type=OptionType.INTEGER)
    @slash_option(name="discord",
                  description="Linked Discord user",
                  required=False,
                  opt_type=OptionType.USER)
    @slash_option(name="game_mode",
                  description="Game mode",
                  required=False,
                  opt_type=OptionType.STRING,
                  choices=[
                        SlashCommandChoice(name="osu!",
                                           value="Standard"),
                        SlashCommandChoice(name="osu! (+AP)",
                                           value="AutopilotStandard"),
                        SlashCommandChoice(name="osu! (+RX)",
                                           value="RelaxStandard"),
                        SlashCommandChoice(name="osu! (+SV2)",
                                           value="ScoreV2Standard"),
                        SlashCommandChoice(name="osu!mania",
                                           value="Mania"),
                        SlashCommandChoice(name="osu!mania (+SV2)",
                                           value="ScoreV2Mania"),
                        SlashCommandChoice(name="osu!taiko",
                                           value="Taiko"),
                        SlashCommandChoice(name="osu!taiko (+RX)",
                                           value="RelaxTaiko"),
                        SlashCommandChoice(name="osu!taiko (+SV2)",
                                           value="ScoreV2Taiko"),
                        SlashCommandChoice(name="osu!catch",
                                           value="CatchTheBeat"),
                        SlashCommandChoice(name="osu!catch (+RX)",
                                           value="RelaxCatchTheBeat"),
                        SlashCommandChoice(name="osu!catch (+SV2)",
                                           value="ScoreV2CatchTheBeat")
                  ])
    async def rs_command(self, ctx: SlashContext, user_id: int = None, discord: Member = None, game_mode: str = None):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /rs")

        await ctx.defer()

        discord_user_id = ctx.author.id
        profile: UserProfile = None

        # response embed
        embed = EmbedBuilder()

        # if discord is specified, override discord_user_id
        if discord:
            discord_user_id = discord.id

        # handle user_id
        if user_id:
            profile = await get_complete_user_profile(user_id, game_mode)

        # handle discord
        if not profile:
            linked = await find_linked_profile(discord_user_id)
            if linked:
                profile = await get_complete_user_profile(linked.user_id, game_mode)
        
        # show error if couldn't find anything
        if not profile:
            embed.set_color(get_config().embed_colors.error)
            embed.set_title(":x: Could not find this user!")
            embed.add_content("Specified user might not have linked their profile yet, or you entered an invalid user ID.\n")
            embed.add_content("If you believe this is an error, feel free to yell at whoever is hosting this right now :3")
        # otherwise, build and show final response
        else:
            # get recent score
            rs = await get_recent_score(profile.user_id, game_mode)

            if not rs:
                embed.set_color(get_config().embed_colors.error)
                embed.set_title("No recent score(s) found")
                embed.add_content("Please go and set a few scores first!!\n")
                embed.add_content("If you believe this is an error, feel free to yell at whoever is hosting this right now :3")
            else:
                embed.set_color(get_config().embed_colors.new_score)
                embed.set_header(f"{profile.user_name} (#{profile.stats.global_rank} - #{profile.stats.country_rank}{profile.country_code})", profile.avatar_url, f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/user/{profile.user_id}?mode={rs.beatmap.mode_name}")
                embed.set_footer(f"{map_sunrise_gamemode_to_sunborne(profile.stats.gamemode)}", get_ruleset_icon_url(profile.stats.gamemode))
                embed.set_thumbnail_image(get_beatmap_cover_image_url(rs.beatmap.set_id, rs.beatmap.diff_id))
                embed.set_title(f"{beatmap_status_name_to_emoji(rs.beatmap.status)} {rs.beatmap.artist} - {rs.beatmap.title} [{rs.beatmap.diff}] ({round(rs.beatmap.stats.sr, 2)} {get_config().emojis.sr})", f"https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/beatmapsets/{rs.beatmap.set_id}/{rs.beatmap.diff_id}")
                embed.add_content(f"{grade_to_emoji(rs.grade)} {str(rs.mods).replace("None", "")} (<t:{round(rs.date.timestamp())}:R>)")
                embed.add_field("Score", f"{rs.score:,}", True)
                embed.add_field("Accuracy", f"{round(rs.accuracy, 2)}%", True)
                embed.add_field("pp", str(round(rs.pp)), True)
                embed.add_field("Combo", f"**x{rs.max_combo}** / {rs.beatmap.stats.max_combo}", True)
                embed.add_field("Stats", f"{get_config().emojis.judge_300} {rs.count_300} · {get_config().emojis.judge_100} {rs.count_100} · {get_config().emojis.judge_50} {rs.count_50} · {get_config().emojis.judge_miss} {rs.count_miss}", True)

        # send embed
        await ctx.send(embed=embed.build())