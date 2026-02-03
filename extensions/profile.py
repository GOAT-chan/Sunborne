from api.user import get_complete_user_profile
from models.user import UserProfile
from utils.logger import Logger
from utils.embeds import EmbedBuilder
from utils.config import get_config
from utils.db import find_linked_profile
from utils.misc import get_badges, get_ruleset_icon_url, map_sunrise_gamemode_to_sunborne
from interactions import Extension, SlashContext, OptionType, Member, SlashCommandChoice, slash_command, slash_option

class ProfileExtension(Extension):
    @slash_command(name="profile",
                   description="Check a GOAT-chan profile")
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
    async def profile_command(self, ctx: SlashContext, user_id: int = None, discord: Member = None, game_mode: str = None):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /profile")

        ctx.defer()

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
        if discord and not profile:
            linked = find_linked_profile(discord_user_id)
            if linked:
                profile = await get_complete_user_profile(linked.user_id)
        
        # show error if couldn't find anything
        if not profile:
            embed.set_color(get_config().embed_colors.error)
            embed.set_title(":x: Could not find this user!")
            embed.add_content("Specified user might not have linked their profile yet, or you entered an invalid user ID.\n")
            embed.add_content("If you believe this is an error, feel free to yell at whoever is hosting this right now :3")
        # otherwise, build and show final response
        else:
            embed.set_title("Profile")
            embed.set_color(get_config().embed_colors.success)
            embed.set_thumbnail_image(profile.avatar_url)
            embed.set_image(profile.banner_url)
            embed.set_header(f"{profile.user_name} ({profile.status})", f"https://flagsapi.com/{profile.country_code}/flat/64.png")
            embed.set_footer(f"{map_sunrise_gamemode_to_sunborne(profile.stats.gamemode)}", get_ruleset_icon_url(profile.stats.gamemode))
            embed.add_field("Registered", f"<t:{round(profile.registration_date.timestamp())}:D>", True)
            embed.add_field("Last Online", f"<t:{round(profile.last_online.timestamp())}:D>", True)
            embed.add_field("Ranking", f"#{profile.stats.global_rank} (#{profile.stats.country_rank})", True)
            embed.add_field("Grades", f"{get_config().emojis.xh_rank} {profile.stats.grades.rank_xh} {get_config().emojis.x_rank} {profile.stats.grades.rank_x} {get_config().emojis.sh_rank} {profile.stats.grades.rank_sh} {get_config().emojis.s_rank} {profile.stats.grades.rank_s} {get_config().emojis.a_rank} {profile.stats.grades.rank_a}")
            embed.add_field("Roles", get_badges(profile.badges), True)
            embed.add_field("Medals", str(profile.stats.medals), True)
            embed.add_field("pp", str(round(profile.stats.total_pp)), True)

        # send embed
        await ctx.send(embed=embed.build())