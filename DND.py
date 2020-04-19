import discord
import random
from discord.ext import commands
import os
import datetime

TOKEN = open('token.txt').readline()
def localRoll(numDie, die):
    if numDie > 10:
        return "too many dice"
    sum = 0
    rolls = 0
    #d4 d6 d8 d10 d12 d20 d100
    while rolls < numDie:
        theDie = die.upper()
        if(theDie=='D4' or die=='d4'):
            sum+= random.randint(1,4)
            rolls+=1
        elif(theDie=='D6' or die=='d6'):
            sum+= random.randint(1,6)
            rolls+=1
        elif(theDie=='D8' or die=='d8'):
            sum+= random.randint(1,8)
            rolls+=1
        elif(theDie=='D10' or die=='d10'):
            sum+= random.randint(1,10)
            rolls+=1
        elif(theDie=='D12' or die=='d12'):
            sum+= random.randint(1,12)
            rolls+=1
        elif(theDie=='D20' or die=='d20'):
            sum+= random.randint(1,20)
            rolls+=1
        elif(theDie=='D100' or die=='d100'):
            sum+= random.randint(1,100)
            rolls+=1
        else:
            return "Something went wrong"
    if(sum==20 and theDie=='D20'):
        return 'Nat 20'
    return sum

client = commands.Bot(command_prefix='!')
client.remove_command('help')
up = 0;

@client.event
async def on_ready():
    global up
    up = datetime.datetime.now()
    os.system('clear')
    print('Bot is ready')
    
@client.event
async def on_member_join(member):
    print(f'{member} has joind the server')
    
@client.event
async def on_member_removes(member):
    print(f'{member} is no longer here')

@client.command()
async def up(ctx):
    global up
    await ctx.send(f'Up since {up} UTC')


@client.command()
async def ping(ctx):
    print(f'{ctx.channel.id}')
    await ctx.send(f'Pong!')
    
@client.command()
async def roll(ctx,die, numDie=1):
    message = localRoll(int(numDie),die)
    if ctx.channel.name == 'general':
         await ctx.send(f'This action is not allowed in {ctx.channel}')
    elif message == "too many dice" or message =="Something went wrong":
        await ctx.send(message)
    else:
        await ctx.send(f' {ctx.author.nick} rolled {localRoll(int(numDie), die)} from {numDie} {die}')

@client.command()
async def clear(ctx, amount=100):
    admin = False
    for role in ctx.author.roles:
        if str(role) == "Admin":
            admin = True
    if admin:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared by {ctx.author.nick}')
    else:
        await ctx.send(type(ctx.author.roles[0]))
        
    
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
async def kill(ctx):
    manager = False
    for role in ctx.author.roles:
        if str(role) == "Bot Manager":
            manager = True
    if manager:
        await ctx.send('Goodbye cruel world')
        exit()
    else:
        await ctx.send('You must be bot manager to perform this task')
       
##@client.command()
##async def help(ctx):
##    await ctx.send('To call me use \'!\'')
##    await ctx.send('**help** : to see this message')
##    await ctx.send('**ping** : A fun little game')
##    await ctx.send('**roll** `d4, d6, d8, d10, d12, d20, d100` `numer of die to roll` ***1 if not specified*** : rolls the specified die the specified amount of times')
##    await ctx.send('**roles** : your highest role')

@client.command()
async def help(ctx):
    author = ctx.author
    embed = discord.Embed(
            color = discord.Colour.orange(),
            title='Help'
    )
    #embed.set_author(name='help')
    embed.add_field(name='!help', value='This message',inline=False)
    embed.add_field(name='!ping', value='Returns Pong!',inline=False)
    embed.add_field(name='!roll', value='Takes in [d4, d6, d8, d10, d12, d20, d100] followed by a number <10 [1 if not specified] and returns the value rolled',inline=False)
    embed.add_field(name='!roles', value='Returns Your roles',inline=False)
    embed.add_field(name='!poop', value='Returns poopy',inline=False)
    
    await ctx.channel.send(embed=embed)
                    

    
    
client.run(TOKEN)



