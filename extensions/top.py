import os

from api.score import get_top_scores
from api.user import get_top_players
from utils.logger import Logger
from utils.embeds import EmbedBuilder
from utils.config import get_config
from utils.misc import get_ruleset_icon_emoji, grade_to_emoji, map_sunrise_gamemode_to_sunborne
from interactions import Extension, SlashContext, slash_command

class TopExtension(Extension):
    @slash_command(name="top-plays",
                   description="Check #1 score in every gamemode")
    async def top_plays_command(self, ctx: SlashContext):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /top-plays")

        await ctx.defer()

        scores = await get_top_scores()

        embed = EmbedBuilder()
        embed.set_color(get_config().embed_colors.success)
        embed.set_title("GOAT-chan Top Plays")

        # build for each top plays
        for score in scores:
            field_text = f"""[{score.beatmap.artist} - {score.beatmap.title} [{score.beatmap.diff}] ({round(score.beatmap.stats.sr, 2)} {get_config().emojis.sr})](https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/score/{score.score_id})
             · {grade_to_emoji(score.grade)} `{score.score:,}` `{round(score.accuracy, 2)}%` `{round(score.pp)}pp` {score.mods}
             · Set by [{score.user.user_name}](https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/user/{score.user.user_id}) on <t:{round(score.date.timestamp())}:D>
            """
            embed.add_field(f"{get_ruleset_icon_emoji(score.gamemode)} {map_sunrise_gamemode_to_sunborne(score.gamemode)}", field_text)

        await ctx.send(embed=embed.build())

    @slash_command(name="top-players",
                   description="Check #1 player in every gamemode")
    async def top_players_command(self, ctx: SlashContext):
        Logger.info(f"user {ctx.author.id} ({ctx.author.display_name}) invoked /top-players")

        await ctx.defer()

        players = await get_top_players()

        embed = EmbedBuilder()
        embed.set_color(get_config().embed_colors.success)
        embed.set_title("GOAT-chan Top Players")

        for player in players:
            field_text = f"""[{player.user_name}](https://{os.environ.get("SUNBORNE_SERVER_DOMAIN")}/user/{player.user_id})
             · Joined <t:{round(player.registration_date.timestamp())}:D>
             · `{round(player.stats.total_pp):,}pp` `{round(player.stats.accuracy, 2)}%` `{player.stats.play_count} plays`
            """
            embed.add_field(f"{get_ruleset_icon_emoji(player.default_gamemode)} {map_sunrise_gamemode_to_sunborne(player.default_gamemode)}", field_text, True)

        await ctx.send(embed=embed.build())