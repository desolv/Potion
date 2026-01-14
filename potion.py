import asyncio
import os
import platform
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from backend import db

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


async def backend():
    try:
        db.init(os.environ["POSTGRES"])
        await db.init_models()
        await db.ping()
        print(f"Running Postgres with SQLAlchemy")
    except Exception as e:
        print(f"Failed to connect to Postgres -> {e}")
        sys.exit(1)


async def main():
    await backend()
    await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
