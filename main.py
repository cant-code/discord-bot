import discord
from discord.ext import commands
from discord import ClientException
import os
import audioread
from time import sleep

from cogs.audio_cog import audio_cog

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

bot.add_cog(audio_cog(bot))

vc = None


@bot.command()
async def fuckyou(ctx, member: discord.Member=None):
  try:
    await ctx.channel.send("Yeah, fuck you {}".format(member.mention))
  except:
    await ctx.channel.send("No, fuck you {}".format(ctx.author.mention))


@bot.command()
async def join(ctx):
  global vc
  try:
    channel = ctx.author.voice.channel
    vc = await channel.connect()
  except AttributeError:
    await ctx.channel.send("You should be in a voice channel to add the bot")
  except ClientException:
    await ctx.channel.send("Bot already in a channel")


@bot.command()
async def dc(ctx):
  try:
    await ctx.voice_client.disconnect()
  except:
    await ctx.channel.send("Bot not connected")


@bot.command()
async def help(ctx):
  embed = discord.Embed(
    colour = discord.Colour.purple()
  )

  embed.set_author(name='Help')
  embed.add_field(name='$join', value="Bot Joins the voice channel", inline=False)
  embed.add_field(name="$arigato", value="Plays the arigato audio", inline=False)
  embed.add_field(name="$hajime", value="Plays the Hajime audio", inline=False)
  embed.add_field(name="$dc", value="Disconnects the bot from the voice channel", inline=False)

  await ctx.channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    path = r"./sounds/hajime.mp3" if member.guild.id == 455010130854019075 else r"./sounds/sound.mp3"

    vc_before = before.channel
    vc_after = after.channel
    global vc
    if vc_before == vc_after:
        return
    if vc_before is not None and vc_after is None:
      if len(vc_before.members) == 1:
        await member.guild.voice_client.disconnect()
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