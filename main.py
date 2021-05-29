import discord
from discord.ext import commands
from discord import ClientException
import os
import audioread
from time import sleep
from keep_alive import keep_alive
from replit import db

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

vc = None


def update_audio(id, audio):
  db[id] = audio


def get_audio(id):
  if id in db.keys():
    return db[id]
  return r"sound.mp3"


@bot.command()
async def join(ctx):
  try:
    channel = ctx.author.voice.channel
    await channel.connect()
  except AttributeError:
    await ctx.channel.send("You should be in a voice channel to add the bot")
  except ClientException:
    await ctx.channel.send("Bot already in a channel")


@bot.command()
async def hajime(ctx):
  try:
    path = r"./sounds/hajime.mp3"
    ctx.voice_client.play(discord.FFmpegPCMAudio(path))
  except AttributeError:
    await ctx.invoke(bot.get_command(name='join'))
    await ctx.reinvoke()
  except ClientException:
    await ctx.channel.send("Audio already playing")


@bot.command()
async def arigato(ctx):
  try:
    path = r"./sounds/arigato.mp3"
    ctx.voice_client.play(discord.FFmpegPCMAudio(path))
  except AttributeError:
    await ctx.invoke(bot.get_command(name='join'))
    await ctx.reinvoke()
  except ClientException:
    await ctx.channel.send("Audio already playing")


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
    if vc_before is None:
        channel = member.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(path))
        with audioread.audio_open(path) as f:
            sleep(f.duration)
        await vc.disconnect()

    elif vc_after is None:
        return
    else:
        channel = member.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(path))
        with audioread.audio_open(path) as f:
          sleep(f.duration)
        await vc.disconnect()


@bot.event
async def on_message(message):
  global vc
  if message.author == bot.user:
    return
  
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$guild'):
    await message.channel.send('Message from {0}'.format(message.guild.name))
  await bot.process_commands(message)


keep_alive()
bot.run(os.environ['TOKEN'])