import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string


version = "Build 3.4"


TOKEN = open('token.txt').readline()
def buildEmbed():
    embed = discord.Embed(
            color = discord.Colour.orange(),
            title='Help'
    )
    embed.add_field(name='!help', value='This message',inline=False)
    embed.add_field(name='!ping', value='Returns Pong!',inline=False)
    embed.add_field(name='!roll', value='Takes in [d4, d6, d8, d10, d12, d20, d100] followed by a number <10 [1 if not specified] and returns the value rolled',inline=False)
    embed.add_field(name='!roles', value='Returns Your roles',inline=False)
    embed.add_field(name='!poop', value='Returns poopy',inline=False)
    embed.add_field(name='!unshitmypants', value='Does the thing', inline=False)
    embed.add_field(name='!flip', value='Flips a coin (Heads or Tails)', inline=False)
    return embed

def checkConditionTrue(cond, comp):
    if(cond == comp):
        return True
    else:
        return False
def checkRole(ctx,desiredRole):
    ans = False
    for role in ctx.author.roles:
        if(checkConditionTrue(str(role), desiredRole)):
            ans = True
    return ans

def localRoll(ctx, numDie, die):
    dice = [4,6,8,10,12,20,100]
    checkAdmin = checkRole(ctx, "Admin")
    if numDie > 10 and checkAdmin == False:
        return "too many dice"
    sum = 0
    rolls = 0
    theDie = int(die[1:])
    #d4 d6 d8 d10 d12 d20 d100
    if theDie in dice:
        while rolls < numDie:
            sum+=random.randint(1,theDie)
            rolls+=1
    else:
        return "Something went wrong"
    if(sum==20 and theDie == 20):
        return 'Nat 20'
    if(sum==1):
        return 'Crit Fail'
    return sum

client = commands.Bot(command_prefix='!')
client.remove_command('help')
processID = psutil.Process(os.getpid())

up = 0
inProgress = False


def getBotStat():
    sendTo = ''
    text_channel_list = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    for channel in text_channel_list:
        if(channel.name == 'bot-status'):
            sendTo = channel
    return sendTo

@client.event
async def on_message(message):
    #print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    text = []
    for str in message.content.upper().split():
        text.append(str.translate(str.maketrans('', '', string.punctuation)))
    for x in text:
        if x == 'BOT' and (message.author.name != 'DND OVERLORD'):
            await message.channel.send('I am the DND Overlord!')
    await client.process_commands(message)

@client.event
async def on_ready():
    global up
    up = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(processID.create_time()))
    os.system('clear')
    print(version)
    print('Bot is ready')
    await getBotStat().purge(limit=1000)
    await getBotStat().send(f'I have arrived with {version} loaded')
    await getBotStat().send(embed=buildEmbed())
    await getBotStat().send(f'Boot time:{up}')

@client.event 
async def on_command_error(ctx, error):
    await ctx.send("Sorry that is an unknown command")
    await ctx.send(embed=buildEmbed())
    
@client.event
async def on_member_join(member):
    print(f'{member} has joind the server')
    
@client.event
async def on_member_removes(member):
    print(f'{member} is no longer here')

@client.command()
async def up(ctx):
    global up
    await ctx.send(f'Up since {up}')

@client.command()
async def repeat(ctx, message, amount=1):
    if(checkRole(ctx, 'Admin')):
        count = 0
        send = ''
        while count < amount:
            send += (message + ' ')
            count+=1
        await ctx.send(send)
    else:
        await ctx.send('This fun command is only for Admins sorry :(')

@client.command()
async def ping(ctx):
    print(f'{ctx.channel.id}')
    await ctx.send(f'Pong!')
    
@client.command()
async def roll(ctx,die, numDie=1):
    message = localRoll(ctx, int(numDie),die)
    if checkConditionTrue(ctx.channel.name, 'general'):
         await ctx.send(f'This action is not allowed in {ctx.channel}')
    elif message == "too many dice" or message =="Something went wrong":
        await ctx.send(message)
    else:
        await ctx.send(f' {ctx.author.nick} rolled {localRoll(ctx, int(numDie), die)} from {numDie} {die}')

@client.command()
async def flip(ctx):
    coin = ['Heads','Tails']
    result = random.choice(coin)
    if checkConditionTrue(ctx.channel.name, 'general'):
         await ctx.send(f'This action is not allowed in {ctx.channel}')
    else:
        await ctx.send(result)
    
    

@client.command()
async def clear(ctx, amount=100):
    admin = checkRole(ctx, 'Admin')
    if admin:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared by {ctx.author.nick}')
    else:
        await ctx.send(f'Only Admin can perform this task')
        
    
@client.command()
async def roles(ctx):
    for role in ctx.author.roles:
        if str(role) != '@everyone':
            await ctx.send(f'{ctx.author.nick} has role {role}')
    
        
@client.command()
async def poop(ctx):
   # print(f'{ctx.author.name.upper()}')
    if('KUSH' not in ctx.author.name.upper()):
       await ctx.send(f'{ctx.author.nick} is poopy')
    else:
       await ctx.send('Keith is a poopy head')

@client.command()
async def unshitmypants(ctx):
    await ctx.send(file=discord.File('assets/poopPants.jpg'))
       
@client.command()
async def kill(ctx):
    global inProgress
    if not inProgress:
        manager = checkRole(ctx,"Bot Manager")
        if manager:
            await getBotStat().send('Goodbye cruel world!')
            await client.change_presence(status=discord.Status.idle)
            exit()
        else:
            await ctx.send('You must be bot manager to perform this task')
    else:
        await ctx.send('There seems to be a session in progress please wait until it is over to kill me')

       

@client.command()
async def help(ctx):
        await ctx.channel.send(embed=buildEmbed())
                    
@client.command()
async def start(ctx):
    global inProgress
    admin = checkRole(ctx, 'Admin')
    channel = checkConditionTrue(ctx.channel.name, 'wpi-campaign') or checkConditionTrue(ctx.channel.name, 'nmh-campaign')
    if admin:
        if channel:
            await ctx.send('Session Started')
            await client.change_presence(status=discord.Status.online, activity=discord.Game("In session"))
            inProgress = True
        else:
            await ctx.send('Sessions can only be started from within a campaign text channel')
    else:
        await ctx.send('Please ask an Admin to start the session')

@client.command()
async def end(ctx):
    global inProgress
    admin = checkRole(ctx, 'Admin')
    channel = checkConditionTrue(ctx.channel.name, 'wpi-campaign') or checkConditionTrue(ctx.channel.name, 'nmh-campaign')
    if admin:
        if channel:
            await ctx.send('Session Ended')
            await client.change_presence(status=discord.Status.idle)
            inProgress = False
        else:
            await ctx.send('Sessions can only be ended from within a campaign text channel')
    else:
        await ctx.send('Please ask an Admin to end the session')
client.run(TOKEN)



