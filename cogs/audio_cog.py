import discord
from discord import app_commands, VoiceClient, Guild
from discord.ext import commands
from discord import ClientException
from discord.utils import get
from yt_dlp import YoutubeDL

class audio_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.YDL_OPTIONS = {'format': 'bestaudio'}

        self.items = []

        self.ydl = YoutubeDL(self.YDL_OPTIONS)


    def search_yt(self, url) -> dict:
        try:
            info = self.ydl.extract_info(url=url, download=False)
        except Exception: 
            return None
        
        print(info['url'])

        return {'source': info['url'], 'title': info['title']}


    def play_next(self, voice_client: VoiceClient):
        if len(self.items) > 0:
            item = self.items.pop(0)
            url = item['source']
            voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: self.play_next(voice_client))


    def get_voice_client(self, guild: Guild) -> VoiceClient | None:
        return get(self.bot.voice_clients, guild=guild)
    

    def check_is_connected(self, vc: VoiceClient) -> bool:
        return vc is not None and vc.is_connected()

    
    async def connect_to_channel(self, interaction: discord.Interaction) -> VoiceClient:
        voice_client = self.get_voice_client(interaction.guild)

        if not voice_client:
            return await interaction.user.voice.channel.connect()
        else:
            return voice_client


    async def play_audio(self, interaction: discord.Interaction):
        item = self.items.pop(0)

        url = item['source']
        vc = await self.connect_to_channel(interaction=interaction)

        try:
            vc.play(source=discord.FFmpegPCMAudio(url), after=lambda e: self.play_next(vc))
        except ClientException:
            await interaction.response.send_message("Audio already playing or not connected to channel")


    @app_commands.command(name="play", description="Play youtube video/audio or playlist")
    async def play(self, interaction: discord.Interaction, link: str):
        # query = " ".join(args)

        audio = self.search_yt(link)
        if audio is None:
            await interaction.response.send_message("Could not play the audio.")
        else:
            self.items.append(audio)
            await self.play_audio(interaction=interaction)


    @app_commands.command(name="pause", description="Pause")
    async def pause(self, interaction: discord.Interaction):
        vc = self.get_voice_client(interaction.guild)
        if self.check_is_connected(vc) and vc.is_playing():
            vc.pause()
        else:
            await interaction.response.send_message("No item to pause")


    @app_commands.command(name="resume", description="Resume")
    async def resume(self, interaction: discord.Interaction):
        vc = self.get_voice_client(interaction.guild)
        if self.check_is_connected(vc) and vc.is_paused():
            vc.resume()
        else:
            await interaction.response.send_message("No item to resume")


    @app_commands.command(name="stop", description="Stop")
    async def stop(self, interaction: discord.Interaction):
        vc = self.get_voice_client(interaction.guild)
        if self.check_is_connected(vc) and (vc.is_paused() or vc.is_playing):
            vc.stop()
        else:
            await interaction.response.send_message("No item currently playing")


    @app_commands.command(name="skip", description="Skip")
    async def skip(self, interaction: discord.Interaction):
        vc = self.get_voice_client(interaction.guild)
        if self.check_is_connected(vc) and vc.is_playing():
            vc.stop()
            self.play_next(interaction)
        else:
            await interaction.response.send_message("No item currently playing")


    @app_commands.command(name="queue", description="Check queue")
    async def queue(self, interaction: discord.Interaction):
        if len(self.items) > 0:
            embed = discord.Embed(
                colour = discord.Colour.purple()
            )

            embed.set_author(name='List')
            for i in self.items: embed.add_field(name=i['title'], inline=False)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Queue is empty")

    
    @app_commands.command(name="onichan", description="Play oni-chan")
    async def onichan(self, interaction: discord.Interaction):
        url = 'https://www.youtube.com/watch?v=skJt3DLHB2A'

        audio = self.search_yt(url)
        if audio is None:
            await interaction.response.send_message("Could not download the audio.")
        else:
            self.items.append(audio)
            await self.play_audio(interaction)


    @app_commands.command(name="hajime", description="Play hajime")
    async def hajime(self, interaction: discord.Interaction):
        self.items.append({'source': r"./sounds/hajime.mp3", 'title': 'Hajime'})
        await self.play_audio(interaction)



    @app_commands.command(name="arigato", description="Play arigato")
    async def arigato(self, interaction: discord.Interaction):
        self.items.append({'source': r"./sounds/arigato.mp3", 'title': 'Arigato'})
        await self.play_audio(interaction)
