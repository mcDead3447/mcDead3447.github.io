import asyncio
import discord
import discord.types.member
from discord.ext import commands
from discord.utils import get
import json
import datetime


class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog [antispam] loaded.")
        while True:
            await asyncio.sleep(10)
            with open("spam_detect.txt", "+r") as file:
                file.truncate(0)

    @commands.Cog.listener()
    async def on_message(self, message):
        counter = 0
        with open("spam_detect.txt", "+r") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            file.writelines(f"{str(message.author.id)}\n")
            if counter > 5:
                await message.author.timeout(datetime.timedelta(seconds=5), reason="Спам")
                with open('user.json', 'r') as f:
                    data = json.load(f)
                    f.close()
                with open('user.json', 'w') as f:
                    data[str(message.author.id)]['SPAM'] += 1
                    json.dump(data, f, indent=4)

                    f.close()
                emb = discord.Embed(
                    title="Нарушение",
                    color=0xff0000,
                    description=f"*У нарушителя было уже {data[str(message.author.id)]['SPAM'] - 1} нарушений, после "
                                f"5 он будет забанен!*",
                    timestamp=message.created_at
                )
                emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
                emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
                emb.add_field(name="Тип нарушения:", value="Спам", inline=True)

                await get(message.guild.text_channels, id=1100402373932896268).send(embed=emb)

                if data[str(message.author.id)]['SPAM'] >= 5:
                    await message.author.ban(reason="Вы привысили допустимое количество нарушений!")
                print("Spam happens[log]")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, messages: int):
        await ctx.defer()
        z = await ctx.channel.purge(limit=messages)
        await asyncio.sleep(1)
        await ctx.send(f"Было удалено {len(z)} сообщений.")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))
