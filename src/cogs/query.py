from discord import Interaction, app_commands, Embed
from db.api import query_account, Account
from discord.ext import commands


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(QueryCog(bot))


class QueryCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command()
    async def balance(self, ctx: Interaction) -> None:
        coins = query_account(ctx.user.id, (Account.BALANCE))
        if coins is None:
            await ctx.response.send_message("oof, couldn't access account")
            return

        await ctx.response.send_message(f"you have {coins} coins")
