import discord
import random
from discord.ext import commands
import os
import time
import psutil
import datetime
import string

version = "Build 3.10"


TOKEN = open('token.txt').readline()

#builds the embed to be sent for the !help command
def helpEmbed():
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
    embed.add_field(name='!statusreport', value='reports status', inline=False)

    return embed

def checkRole(ctx,desiredRole):
    ans = False
    for role in ctx.author.roles:
        if str(role) == desiredRole:
            ans = True
    return ans

#Rolls the desiered amount of die and returns the list of rolls and their sum
def localRoll(ctx, numDie, die):
    dice = [4,6,8,10,12,20,100]
    checkAdmin = checkRole(ctx, "Admin")
    if numDie > 40 and checkAdmin == False:
        return "too many dice"
    values = []
    sum = 0
    rolls = 0
    theDie = int(die[1:])
    #d4 d6 d8 d10 d12 d20 d100
    if theDie in dice:
        while rolls < numDie:
            roll = random.randint(1,theDie)
            sum+= roll
            values.append(roll)
            rolls+=1
    else:
        return "Something went wrong"
    if(sum==20 and theDie == 20 and numDie==1):
        return ('Nat 20',values)
    if(sum==1):
        return ('Crit Fail', values)
    return (sum,values)

client = commands.Bot(command_prefix='!')
client.remove_command('help')
processID = psutil.Process(os.getpid())

up = 0
inProgress = False

#gets the BotStat channel
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

#logs all messages on server 
@client.event
async def on_message(message):

    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    text = []
    for str in message.content.upper().split():
        text.append(str.translate(str.maketrans('', '', string.punctuation)))
    for x in text:

        if (x == 'BOT' or x==message.guild.me.display_name.upper()) and (message.author.display_name != message.guild.me.display_name):
            await message.channel.send(f'I am the {message.guild.me.display_name}!')
    await client.process_commands(message)
    

#sets up bot and notifies server
@client.event
async def on_ready():
    global up
    up = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(processID.create_time()))
    os.system('clear')
    print(version)
    print('Bot is ready')
    channel = getBotStat()
    await channel.purge(limit=1000)
    await channel.send(f'I have arrived with {version} loaded')
    await channel.send(embed=helpEmbed())
    await channel.send(f'Boot time:{up}')


#sends help on incorrect command/syntax
@client.event 
async def on_command_error(ctx, error):
    await ctx.send("Sorry that is an unknown command")
    await ctx.send(embed=helpEmbed())
    
@client.event
async def on_member_join(member):
    print(f'{member} has joind the server')
    
@client.event
async def on_member_removes(member):
    print(f'{member} is no longer here')

#returns uptime to server
@client.command()
async def up(ctx):
    global up
    await ctx.send(f'Up since {up}')
    
@client.command()
async def mr(ctx):
    wet = ['dank','moist','sopping','slimy','slippery','soggy','soaking','drenched','aqueous','dripping','dewy','watery','doused','fluidy','sodden','soggy','water-logged','watered-down','damp','juicy','viscous','sappy','fluidic','molten','sloppy','oily','liquidy','oozy','sappy','syrupy','lubricated','un-dry','oceanic','un-dammed','flowing','mucousy','humid','clamy','misty','washed out']
    wet.sort()

    mouth = ['lips','tongue','face','throat','teeth','gums','uvula','gullet','wind pipe','hole','orifice','crevice','cavity','kisser','yap','gob','opening','rim','chops','cheeks','mug','crack','gap','pit','tunnel','chasm','skin','passage','slit','vent','split','jowl','gill','mandible','palate','tonsil','jaws','muzzle','maw','esophagus']
    mouth.sort()

    string = "Mr." + random.choice(wet).capitalize() + '-' + random.choice(mouth).capitalize()
    await ctx.send(string)

#repeats the given message {amount} times
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
    
#rolls the {die} {numDie} times
@client.command()
async def roll(ctx,die, numDie=1):
    tup = localRoll(ctx, int(numDie),die)

    if ctx.channel.topic == 'general chat':

         await ctx.send(f'This action is not allowed in {ctx.channel}')
    elif tup == "too many dice" or tup =="Something went wrong":
        await ctx.send(tup)
    else:
        await ctx.send(f' {ctx.author.display_name} rolled {tup[0]} from {numDie} {die} \n{tup[1]}')

@client.command()
async def blast(ctx):
    first = localRoll(ctx, 3, 'd20')
    second = localRoll(ctx, 1, 'd10')
    await ctx.send(f' {ctx.author.display_name} rolled {first[0]} + 13 from 3 d20 \n{first[1]}')
    await ctx.send(f' {ctx.author.display_name} rolled {second[0]} + 12 from 1 d10 \n{second[1]}')
    await ctx.send(f'Eldritch blast with Trofs stats is {first[0] + 13} to hit and  {second[0] + 12} damage')


#flips a coin
@client.command()
async def flip(ctx):
    coin = ['Heads','Tails']
    result = random.choice(coin)
    await ctx.send(result)

    
    
#clears message history from channel
@client.command()
async def clear(ctx, amount=100):
    admin = checkRole(ctx, 'Admin')
    if admin:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared by {ctx.author.display_name}')
    else:
        await ctx.send(f'Only Admin can perform this task')
        
#returns authors roles on the server
@client.command()
async def roles(ctx):
    for role in ctx.author.roles:
        if str(role) != '@everyone':
            await ctx.send(f'{ctx.author.display_name} has role {role}')


#returns the zoom link for the sessions
@client.command()
async def zoom(ctx):
    link = 'https://wpi.zoom.us/j/2284559997'
    await ctx.send(link)
    

    
#calls the author a poopy head 
@client.command()
async def poop(ctx):
   # print(f'{ctx.author.name.upper()}')
    if('KUSH' not in ctx.author.name.upper()):
       await ctx.send(f'{ctx.author.display_name} is poopy')
    else:
       await ctx.send('Keith is a poopy head')

#returns image
@client.command()
async def unshitmypants(ctx):
    await ctx.send(file=discord.File('assets/poopPants.jpg'))
       
#kills the bot
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
async def statusreport(ctx):
    subject = random.choice(ctx.guild.members)
    report = discord.Embed(
        color = discord.Colour.dark_red(),
        title='STATUS REPORT'
    )
    

    report.add_field(name='Status:', value=f'{subject.status}',inline=False)
    report.add_field(name=f'{subject.display_name}:', value='Still poopy',inline=False)

    report.add_field(name='Next: ',value='Will update when status changes',inline=False)
    await ctx.send(embed=report)

       
#sends the help EMbed
@client.command()
async def help(ctx):
        await ctx.channel.send(embed=helpEmbed())


#starts the server so that the bot can't be killed when in session and sets bot status            
@client.command()
async def start(ctx):
    global inProgress
    admin = checkRole(ctx, 'Admin')
    channel = ctx.channel.topic == 'campaign'

    if admin:
        if channel:
            await ctx.send('Session Started')
            await client.change_presence(status=discord.Status.online, activity=discord.Game("In session"))
            inProgress = True
        else:
            await ctx.send('Sessions can only be started from within a campaign text channel')
    else:
        await ctx.send('Please ask an Admin to start the session')

#end sthe session so that the bot can be killed and resets the bot status
@client.command()
async def end(ctx):
    global inProgress
    admin = checkRole(ctx, 'Admin')
    channel = ctx.channel.topic == 'campaign'

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



