import discord
from discord.app_commands import MissingPermissions
from discord.ext import commands
from discord.utils import get
import os
import json


class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BADWORDS = ["мат1", "мат2"]
        self.LINKS = ["https", "http", "://"]

    if not os.path.exists('user.json'):
        with open('user.json', 'w') as file:
            file.write('{}')
            file.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog [bans] loaded.")
        for guild in self.bot.guilds:
            for member in guild.members:
                with open('user.json', 'r') as file:
                    data = json.load(file)

                with open('user.json', 'w') as file:
                    data[str(member.id)] = {
                        "WARNS": 0,
                        "SPAM": 0
                    }
                    file.write(json.dumps(data, indent=4))
                    file.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        WARN = self.BADWORDS + self.LINKS

        for i in range(0, len(WARN)):
            if WARN[i] in message.content.lower():
                with open('user.json', 'r') as file:
                    data = json.load(file)
                    file.close()
                with open('user.json', 'w') as file:
                    data[str(message.author.id)]['WARNS'] += 1
                    json.dump(data, file, indent=4)

                    file.close()
                emb = discord.Embed(
                    title="Нарушение",
                    color=0xff0000,
                    description=f"*У нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1} нарушений, после "
                                f"5 он будет забанен!*",
                    timestamp=message.created_at
                )
                emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
                emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
                emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

                await get(message.guild.text_channels, id=1100402373932896268).send(embed=emb)

                if data[str(message.author.id)]['WARNS'] >= 5:
                    await message.author.ban(reason="Вы привысили допустимое количество нарушений!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "Причины отсутствуют."
        await ctx.guild.kick(member)
        await ctx.reply(embed=discord.Embed(
            color=0xff0000,
            title=f"Пользователь {member} был кикнут с сервера",
            description=f"По причине: {reason}"))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "Причины отсутствуют."
        await ctx.guild.ban(member)
        await ctx.reply(embed=discord.Embed(
            color=0xff0000,
            title=f"Пользователь {member} был забанен на сервере",
            description=f"По причине: {reason}"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.reply(embed=discord.Embed(
                color=0xff0000,
                title="У тебя недостаточно прав для этого"))
        else:
            print(ctx, error)
            await ctx.reply(embed=discord.Embed(
                color=0xff0000,
                title="У тебя недостаточно прав для этого"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        await channel.send(f"```Добро пожаловать на сервер, {member}!```")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        await channel.send(f"```{member} покинул нас.```")


async def setup(bot):
    await bot.add_cog(Bans(bot))
