import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
from discord.ext.commands import Bot
import asyncio
from discord.utils import get
import time


client = commands.Bot(command_prefix = '.')
message = joined = 0


#__________#when ready__________
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready.')

async def update_stats():
    await client.wait_until_ready()
    global message, joined


#__________#tasks: bot menja svoj status vsakih 5 sekund__________
status = cycle(['dnd','idle', 'online'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status(next(status)), activity=discord.Game('Online and working'))


#__________#notices a member joining__________
@client.event
async def on_member_join(member):
    channel = client.get_channel(482460935110393861)
    await channel.send('hello')
    print(f'{member} has joined the server.')


#__________#notices a member leaving__________
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


#__________#unknown command error__________
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You used a command that I don't like.")


#__________#ping command__________
@client.command()
async def ping(ctx):
    await ctx.send(f'PONG!! {round(client.latency * 1000)}ms')


#__________#8ball command__________
@client.command(aliases=['8ball'])
async def _8ball(ctx, *,question):
    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                "Don't count on it.",
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forgot to ask me something.")


#__________#clear chat__________
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


#__________#kick command__________
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


#__________#ban command__________
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


#__________#unban command__________
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    memeber_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (memeber_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')


#__________#connects to voice channel__________
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    print ('Joined the channel.')
    await ctx.send(f"The people need me in {channel}")

@join.error
async def join_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("You need to be in a channel to summon me.")


#__________#disconnects from voice channel__________
@client.command(pass_context=True)
async def leave(ctx):

    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./sounds/leave.mp3")
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)

    time.sleep(3)
    server = ctx.message.guild.voice_client
    await server.disconnect()
    print ('Disconnected from the channel.')
    await ctx.send(f"I must leave you now, my Master.")

@leave.error
async def join_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("How can i leave if I am not here.")


#__________#loads opus__________
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

        raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))


#__________#plays soud__________
@client.command()
async def digy(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio(executable="C:/Users/lukak/Desktop/ffmpeg/bin/ffmpeg.exe", source="C:/Users/lukak/Desktop/DiscordBot/sounds/digy.mp3")
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)




client.run('Token')
