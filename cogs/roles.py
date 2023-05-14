import discord
from discord.ext import commands
from discord.ui import View

class ServerRolesChoose(View):
    @discord.ui.select(
        min_values=1,
        max_values=3,
        placeholder='Выбрать роль',
        options=[
            discord.SelectOption(label='Красная роль', emoji="🔴", value='0', description='Тестовая роль'),
            discord.SelectOption(label='Фиолетовая роль', emoji="🟣", value='1', description='Тестовая роль'),
            discord.SelectOption(label='Зелёная роль', emoji="🟢", value='2', description='Тестовая роль')
        ])
    async def select_callback(self, interaction, select):
        server = interaction.guild
        Role_one = discord.utils.get(server.roles, name='Красная роль')
        Role_two = discord.utils.get(server.roles, name='Фиолетовая роль')
        Role_three = discord.utils.get(server.roles, name='Зелёная роль')
        role = None
        if Role_one in interaction.user.roles:
            await interaction.user.remove_roles(Role_one)
        if Role_two in interaction.user.roles:
            await interaction.user.remove_roles(Role_two)
        if '0' in select.values:
            await interaction.user.add_roles(Role_one)
            role = f'{Role_one.mention}'
        if '1' in select.values:
            await interaction.user.add_roles(Role_two)
            if Role_one and Role_two in interaction.user.roles:
                role = f'{Role_one.mention}, {Role_two.mention}'
            else:
                role = f'{Role_two.mention}'
        if '2' in select.values:
            await interaction.user.add_roles(Role_three)
            if Role_one and Role_two and Role_three in interaction.user.roles:
                role = f'{Role_one.mention}, {Role_two.mention}, {Role_three.mention}'
            elif Role_one and Role_three in interaction.user.roles:
                role = f'{Role_one.mention}, {Role_three.mention}'
            elif Role_two and Role_three in interaction.user.roles:
                role = f'{Role_two.mention}, {Role_three.mention}'
            else:
                role = f'{Role_three.mention}'
        if role is None:
            await interaction.response.send_message(f'Вы не выбрали ни одной роли, если у Вас до этого стояли '
                                                    f'какие-либо серверные роли, они были удалены', ephemeral=True)
        else:
            await interaction.response.send_message(f'Теперь у вас следующие серверные роли: {role}',
                                                    ephemeral=True)

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog [roles] loaded.")

    @commands.command()
    async def roles(self, ctx):
        view = ServerRolesChoose()
        await ctx.send("Выберите нужную вам роль.", view=view)

    @commands.command()
    async def пон(self, ctx):
        await ctx.send("пон")

async def setup(bot):
    await bot.add_cog(Roles(bot))