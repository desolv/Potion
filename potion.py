import asyncio
import os
import platform

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(f".env")

bot = commands.Bot(
    command_prefix="?",
    help_command=None,
    intents=discord.Intents.all(),
)

print("Potion Robot")
print(
    f"Running at Python {platform.python_version()}v, "
    f"Discord.py {discord.__version__}v - {platform.system()} {platform.release()} ({os.name})"
)


async def main():
    await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
