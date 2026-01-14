from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handle prefix command errors"""
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            return
        if isinstance(error, commands.ChannelNotFound):
            message = f"⚠️ Invalid channel **{error.argument}** not found!"
        elif isinstance(error, commands.BadArgument):
            message = "⚠️ Invalid argument. Check your input and try again"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"⚠️ Missing argument: `{error.param.name}`"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"⌛ This command is on cooldown. Try again in {error.retry_after:.1f}s"
        else:
            print(f"Command issue at {ctx.guild.id} -> {error}")
            message = f"❌ Something went wrong: {error}"

        await ctx.reply(message, delete_after=10)


async def setup(bot):
    await bot.add_cog(Errors(bot))
