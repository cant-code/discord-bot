import discord
from discord.ext import commands
from discord import ClientException
from youtube_dl import YoutubeDL

class audio_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.item = None

        self.vc = None


    def search_yt(self, url):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % url, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}


    async def play_audio(self, ctx):
        url = getattr(self.item, 'source', self.item)

        try:
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
        except AttributeError:
            await ctx.invoke(self.bot.get_command(name='join'))
            await ctx.reinvoke()
        except ClientException:
            await ctx.channel.send("Audio already playing")

    
    @commands.command()
    async def onichan(self, ctx):
        url = 'https://www.youtube.com/watch?v=skJt3DLHB2A'

        audio = self.search_yt(url)
        if type(audio) == type(True):
            await ctx.send("Could not download the audio.")
        else:
            self.item = audio
            await self.play_audio(ctx)


    @commands.command()
    async def hajime(self, ctx):
        self.item = r"../sounds/hajime.mp3"
        await self.play_audio(ctx)



    @commands.command()
    async def arigato(self, ctx):
        self.item = r"../sounds/arigato.mp3"
        await self.play_audio(ctx)