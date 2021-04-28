import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
from random import randint
import asyncio
import os

# quit and cancel has delay from the asyncio.sleep
# force_quit (maybe also send message to the person that was waiting)

users = {}
bot = commands.Bot(command_prefix ='*')
bot.remove_command('help')

def validate_url(url):
    url1 = 'https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept='
    url2 = '&course='
    url3 = '&section='
    if url1 in url and url2 in url and url3 in url:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            t = soup.find_all('a')
            s = [e.string for e in t]
            if s[23] == "archived versions of the UBC Calendar":
                return False
            return True
        except:
            print('invalid shit')
            return False
    else:
        return False

def validate_user(user_id):
    return not(user_id in users)

def get_link_name(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find('h4')
    return '['+name.string+']'+'('+url+')'

async def send_error_embed(ctx, description):
    embed = discord.Embed(title="Error", description=description, colour=discord.Colour.red())
    await ctx.send(embed=embed)

async def validate_and_monitor(ctx, queue_type, url):
    user_id = ctx.message.author.id
    if validate_url(url):
        if validate_user(user_id):
            users[user_id] = (True, url)
            embed = discord.Embed(title="Started monitoring page",
                                  description='[' + f"{ctx.message.author.mention}] Monitoring " + get_link_name(url),
                                  colour=discord.Colour.green())
            await ctx.send(embed=embed)
            while(users[user_id][0]):
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                strongs = soup.find_all('strong')
                strong_nums = [int(i.string) for i in strongs if i.string.isnumeric()]
                if strong_nums[queue_type] > 0:
                    embed.title = "Seat found"
                    embed.description = ('[' + f"{ctx.message.author.mention}] "
                                               f"Seat found. Don't blame me if you lose your spot :)))\n" +
                                         get_link_name(url))
                    try:
                        await ctx.author.send(embed=embed)
                    except:
                        await ctx.send(embed=embed)
                    break
                await asyncio.sleep((randint(6,8)) * len(users))
            del users[user_id]
        else:
            await send_error_embed(ctx, '[' + f"{ctx.message.author.mention}] You can only track one course at a time")
    else:
        await send_error_embed(ctx, '[' + f"{ctx.message.author.mention}] Invalid link")

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord")

@bot.command (name = 'general')
async def general(ctx, url):
    await(validate_and_monitor(ctx, 2, url))

@bot.command (name = 'any')
async def any(ctx, url):
    await(validate_and_monitor(ctx, 0, url))

@bot.command (name = 'cancel')
async def cancel(ctx):
    user_id = ctx.message.author.id
    if user_id in users:
        if users[user_id][0]:
            print(users[user_id][0])
            temp = list(users[user_id])
            temp[0] = False
            users[user_id] = temp
            embed = discord.Embed(description='[' + f"{ctx.message.author.mention}] Successfully canceled",
                                  colour=discord.Colour.green())
            await ctx.send(embed=embed)
            return
    await send_error_embed(ctx, '[' + f"{ctx.message.author.mention}] You're not monitoring anything right now")

@bot.command (name = 'force_quit')
async def force_quit(ctx, user_id: int):
    author_id = ctx.message.author.id
    if author_id == 100063538223026176:
        if user_id in users:
            embed = discord.Embed(description='[' + f"{ctx.message.author.mention}] Successfully canceled " +
                                              get_link_name(users[user_id][1]), colour=discord.Colour.green())
            temp = list(users[user_id])
            temp[0] = False
            users[user_id] = temp
            await ctx.send(embed=embed)
        else:
            await send_error_embed(ctx,'[' + f"{ctx.message.author.mention}] There's no person with that id ")
    else:
        await send_error_embed(ctx,'[' + f"{ctx.message.author.mention}] You don't have permission to use this command")

@bot.command (name = 'display')
async def display(ctx):
    user_id = ctx.message.author.id
    if user_id == 100063538223026176:
        await ctx.message.author.send('```'+str(users)+'```')
    else:
        await send_error_embed(ctx,'[' + f"{ctx.message.author.mention}] You don't have permission to use this command")

@bot.command (name = 'help')
async def help(ctx):
    await ctx.send('```'+"Commands and how to use them:\n"
                         "\n*general <url>  Pings once a general seat is available"
                         "\n*any <url>      Pings once a general or restricted seat is available"
                         "\n*cancel         Stops monitoring page\n"
                         "\nReplace <url> with any valid UBC course url\n"
                         "\nIf you want the bot to DM you, make sure you allow direct messages from server members "
                         "(You can find this in Privacy & Safety settings). Otherwise, the bot will just ping you in "
                         "the server's chat\n"
                         "\nSide note: I don't know how fast I'm allowed to go without breaking the site's terms of use"
                         " (I've also made it so that speed goes down if more people are using the bot). "
                         "Other notifiers out there might be a few seconds faster. "
                         "So if you have a good spot in the waitlist, be very careful."+'```')

bot.run(os.getenv('TOKEN'))
