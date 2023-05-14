import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()


asyncio.run(main())

bot.run('MTA4NDg5MjYwMTgzODIxMTA5Mg.GTmI1i.Sz2-i47hJMgMlEkhE1D2yKUbYNeBGTGFqVrw8g')