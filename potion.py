# -*- coding: utf-8 -*-
import asyncio
import os
import platform
import sys
from pathlib import Path

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


async def load():
    for root in "commands", "master":
        for extension in Path(root).rglob("*.py"):
            if extension.stem.startswith("__") or any(folder in extension.parts for folder in (".venv", "models")):
                continue

            ext_path = ".".join(extension.with_suffix("").parts)
            try:
                await bot.load_extension(ext_path)
            except commands.NoEntryPointError:
                continue


async def main():
    await backend()
    await load()
    await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())
