import discord
from discord import ClientException, VoiceState
from discord.ext import commands
import os
import audioread
from time import sleep
import sentry_sdk
import logging
from sentry_sdk.integrations.logging import LoggingIntegration

from cogs.audio_cog import audio_cog

sentry_logging = LoggingIntegration(
  level=logging.INFO,
  event_level=logging.ERROR
)

sentry_sdk.init(
  dsn=os.environ['SENTRY_DSN'],
  integrations=[
    sentry_logging
  ],
  traces_sample_rate=1.0,
  environment=os.environ['ENV']
)

class aclient(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix="!", intents=discord.Intents.default())
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    await self.add_cog(audio_cog(self))
    if not self.synced:
      await tree.sync()
      self.synced=True
    print(f"We have logged in as {self.user}.")

bot = aclient()
tree = bot.tree


@tree.command(name="fuckyou", description="Says fuck you")
async def fuckyou(interaction: discord.Interaction, member: discord.Member=None):
  if member is not None:
    await interaction.response.send_message(f"Yeah, fuck you {member.mention}!")
  else:
    await interaction.response.send_message(f"No, fuck you {interaction.user.mention}")


@tree.command(name="join", description="Join channel")
async def join(interaction: discord.Interaction):
  try:
    channel = interaction.user.voice.channel
    await channel.connect()
  except AttributeError:
    await interaction.response.send_message("You should be in a voice channel to add the bot")
  except ClientException:
    await interaction.response.send_message("Bot already in a channel")


@tree.command(name="disconnect", description="Disconnect from channel")
async def dc(interaction: discord.Interaction):
  try:
    await interaction.guild.voice_client.disconnect()
  except:
    await interaction.response.send_message("Bot not connected")


@tree.command(name="help", description="Help")
async def help(interaction: discord.Interaction):
  embed = discord.Embed(
    colour = discord.Colour.purple()
  )

  embed.set_author(name='Help')
  embed.add_field(name='$join', value="Bot Joins the voice channel", inline=False)
  embed.add_field(name="$arigato", value="Plays the arigato audio", inline=False)
  embed.add_field(name="$hajime", value="Plays the Hajime audio", inline=False)
  embed.add_field(name="$dc", value="Disconnects the bot from the voice channel", inline=False)

  await interaction.channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member: discord.Member, before: VoiceState, after: VoiceState):
    path = r"./sounds/hajime.mp3" if member.guild.id == 455010130854019075 else r"./sounds/sound.mp3"
    path = r"./sounds/synthesize.mp3" if member.id == 312084826675216387 else path

    vc_before = before.channel
    vc_after = after.channel
    vc = None

    voice_state = member.guild.voice_client
    if voice_state is not None and len(voice_state.channel.members) == 1:
      await voice_state.disconnect()

    if member.bot:
      return
    
    if vc_before == vc_after:
      return
    if vc_before is not None and vc_after is None:
      pass
    else:
      try:
        channel = member.voice.channel
        vc = await channel.connect()
        if vc is not None:
          vc.play(discord.FFmpegPCMAudio(path))
          with audioread.audio_open(path) as f:
            sleep(f.duration)
          await vc.disconnect()
      except:
        sleep(.5)
        vc.play(discord.FFmpegPCMAudio(path))


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$guild'):
    await message.channel.send('Message from {0}'.format(message.guild.name))
  await bot.process_commands(message)


bot.run(os.environ['TOKEN'])