from api.user import get_complete_user_profile
from database.manager import DbSession
from database.models.user import User
from models.user import UserProfile
from utils.logger import Logger
from utils.embeds import EmbedBuilder
from utils.config import get_config
from utils.db import check_if_user_id_is_claimed, find_linked_profile
from utils.misc import get_badges, get_ruleset_icon_url, map_sunrise_gamemode_to_sunborne
from interactions import Extension, SlashContext, OptionType, Member, SlashCommandChoice, slash_command, slash_option
from datetime import datetime

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
            embed.set_title("Profile")
            embed.set_color(get_config().embed_colors.success)
            embed.set_thumbnail_image(profile.avatar_url)
            embed.add_image(profile.banner_url)
            embed.set_header(f"{profile.user_name} ({profile.status})", f"https://flagsapi.com/{profile.country_code}/flat/64.png")
            embed.set_footer(f"{map_sunrise_gamemode_to_sunborne(profile.stats.gamemode)}", get_ruleset_icon_url(profile.stats.gamemode))
            embed.add_field("Registered", f"<t:{round(profile.registration_date.timestamp())}:D>", True)
            embed.add_field("Last Online", f"<t:{round(profile.last_online.timestamp())}:R>", True)
            embed.add_field("Ranking", f"#{profile.stats.global_rank} (#{profile.stats.country_rank})", True)
            embed.add_field("Grades", f"{get_config().emojis.xh_rank} {profile.stats.grades.rank_xh} {get_config().emojis.x_rank} {profile.stats.grades.rank_x} {get_config().emojis.sh_rank} {profile.stats.grades.rank_sh} {get_config().emojis.s_rank} {profile.stats.grades.rank_s} {get_config().emojis.a_rank} {profile.stats.grades.rank_a}")
            embed.add_field("Roles", get_badges(profile.badges), True)
            embed.add_field("Medals", str(profile.stats.medals), True)
            embed.add_field("pp", str(round(profile.stats.total_pp)), True)

        # send embed
        await ctx.send(embed=embed.build())

    @slash_command(name="link",
                   description="Link your GOAT-chan profile")
    @slash_option(name="user_id",
                  description="User ID",
                  required=True,
                  opt_type=OptionType.INTEGER)
    async def link_command(self, ctx: SlashContext, user_id: int):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /linked")

        await ctx.defer()

        linked_profile = await find_linked_profile(ctx.author.id)

        embed = EmbedBuilder()

        # stop if user linked already
        if linked_profile:
            embed.set_color(get_config().embed_colors.error)
            embed.set_title("You've already linked!")
            embed.add_content("If you messed up and linked the wrong profile, please manually unlink yourself using `/unlink`, then run `/link` again.\n")
            embed.add_content("Please only link ***your*** GOAT-chan profile.")
            await ctx.send(embed=embed.build())
            return
        
        # check if there's a discord user linked with this id yet
        if await check_if_user_id_is_claimed(user_id):
            embed.set_color(get_config().embed_colors.error)
            embed.set_title("Sorry, this profile is linked to another Discord user.")
            embed.add_content("Please make sure the user ID you entered corresponds to your GOAT-chan profile.\n")
            embed.add_content("If you are sure that you've entered the correct profile ID, contact a moderator.")
            await ctx.send(embed=embed.build())
            return
        
        profile = await get_complete_user_profile(user_id)

        if not profile:
            embed.set_color(get_config().embed_colors.error)
            embed.set_title("Couldn't find this user ID.")
            embed.add_content("Please check the user ID that you've entered again.\n")
            embed.add_content("If you are sure that you've entered the correct profile ID, contact a moderator.")
            await ctx.send(embed=embed.build())
            return
        
        # link
        user = User()
        user.discord_id = ctx.author.id
        user.user_id = profile.user_id
        user.user_name = profile.user_name
        user.linked_date = datetime.now()
        user.card_style = 0
        user.embed_style = 0

        # add to db
        session = DbSession()
        await session.add_or_update(user)
        await session.close()

        # config embed
        embed.set_color(get_config().embed_colors.success)
        embed.set_title("Linked successfully!")
        embed.set_thumbnail_image(profile.avatar_url)
        embed.add_content(f"Your Discord account was successfully linked to **{profile.user_name}**!")

        # send
        await ctx.send(embed=embed.build())

    @slash_command(name="unlink",
                   description="Unlink your GOAT-chan profile")
    async def unlink_command(self, ctx: SlashContext):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /unlink")

        await ctx.defer()

        linked_profile = await find_linked_profile(ctx.author.id)

        embed = EmbedBuilder()

        # stop if user havent linked yet
        if not linked_profile:
            embed.set_color(get_config().embed_colors.error)
            embed.set_title("You haven't linked your profile yet!")
            embed.add_content("You can't unlink a profile that you haven't linked yet :wilted_rose:")
            await ctx.send(embed=embed.build())
            return

        # remove from db
        session = DbSession()
        await session.remove(linked_profile)
        await session.close()

        # config embed
        embed.set_color(get_config().embed_colors.success)
        embed.set_title("Unlinked successfully!")
        embed.add_content(f"Your Discord account is no longer linked to **{linked_profile.user_name}**.")

        # send
        await ctx.send(embed=embed.build())
