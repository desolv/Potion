from discord.ext import commands


class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} with {len(self.bot.guilds)} guild(s)")


async def setup(bot: commands.Bot):
    await bot.add_cog(Listeners(bot))
