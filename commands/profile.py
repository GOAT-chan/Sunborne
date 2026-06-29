from loguru import logger
from interactions import Extension, SlashContext, slash_command, slash_option, OptionType, component_callback, ComponentContext
from messages.templates.generic import ErrorMessage, SuccessMessage
from messages.templates.profile import ProfileLinkPromptMessage
from api.adapter import adapter
from cache.cacher import get_profile_linking_data, set_profile_linking_data
from database.manager import database

class ProfileExtension(Extension):
    @slash_command(name="link",
                   description="Link your profile")
    @slash_option(name="user_name",
                  description="Your user name",
                  required=True,
                  opt_type=OptionType.STRING)
    async def link_command(self, ctx: SlashContext, user_name: str):
        logger.info(f"/link was invoked by {ctx.author.username}: user_name={user_name}")
        await ctx.defer(ephemeral=True)
        user = await database.get_user(ctx.author.id)
        if user:
            await ctx.send(components=ErrorMessage.new(f"An account was already linked to this Discord profile, please unlink it before linking another one."))
            return
        user = await adapter.search_users(user_name)
        if not user:
            await ctx.send(components=ErrorMessage.new(f"Could not find user `{user_name}`. Please re-check and try again."))
            return
        await set_profile_linking_data(ctx.author.id, user.id)
        await ctx.send(components=ProfileLinkPromptMessage.new(user))

    @slash_command(name="unlink",
                   description="Unlink your profile")
    async def unlink_command(self, ctx: SlashContext):
        logger.info(f"/unlink was invoked by {ctx.author.username}")
        await ctx.defer(ephemeral=True)
        user = await database.get_user(ctx.author.id)
        if not user:
            await ctx.send(components=ErrorMessage.new("There is no account to unlink."))
            return
        await database.delete_user(ctx.author.id)
        await ctx.send(components=SuccessMessage.new("Your account was unlinked successfully."))

    @component_callback("accept_link_button")
    async def link_button_callback(self, ctx: ComponentContext):
        data = await get_profile_linking_data(ctx.author.id)
        if not data:
            await ctx.edit_origin(components=ErrorMessage.new("Please try running the command again."))
            return
        await database.add_user(ctx.author.id, data)
        await ctx.edit_origin(components=SuccessMessage.new("Your account was linked successfully!"))