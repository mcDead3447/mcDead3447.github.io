import discord
from discord.ext import commands
from discord.utils import get
from yt_dlp import YoutubeDL
import asyncio


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 - reconnect_streames 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    def search(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entires'][0]
            except:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("Невозможно подключиться к голосовому каналу")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
        else:
            self.is_playing = False

    @commands.command()
    async def play_audio(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            vc = await channel.connect()

        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()

        # Load the audio file and play it
        vc.play(discord.FFmpegPCMAudio(url, executable="C:\\ffmpeg\\ffmpeg.exe", **self.FFMPEG_OPTIONS))

        # Wait for the audio to finish playing or for the user to stop it
        while vc.is_playing():
            await asyncio.sleep(1)

        # Disconnect from the voice channel
        await vc.disconnect()

    @commands.command(name="play", aliases=["p", "playing"], help="Музыка блин")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Подключитесь к голосовому каналу.")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search(query)
            if type(song) == type(True):
                await ctx.send("Не удалось загрузить песню.")
            else:
                await ctx.send("Песня добавлена в очередь")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Пауза")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        else:
            self.vc.resume()

    @commands.command(name="pesume", aliases=["r"], help="Продолжить воспроизведение музыки.")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Пропуск песни.")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Просмотр очереди.")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Список очереди пуст.")

    @commands.command(name="cqueue", aliases=["c", "bin"], help="Остановка играющей песни и очистка списка очереди.")
    async def cqueue(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Список очереди очищен.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog [music] loaded.")


async def setup(bot):
    await bot.add_cog(Music(bot))
