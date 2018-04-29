import urllib
import praw
import discord
import asyncio
import pymongo
from random import randint
from discord.ext import commands
from secret import *
#from secret import discordToken, discordClientId, discordDescription, dbpassword
#from secret import PRAWclientId, PRAWclientSecret, PRAWusername, PRAWpassword, PRAWuserAgent


#Create connection to DB
dbclient = pymongo.MongoClient('mongodb+srv://jared_admin:'+ urllib.parse.quote(dbpassword)+'@jared-db-rvwv5.mongodb.net/drbotdrugs')
db = dbclient.drbotdrugs

#Set up bot instance
bot = commands.Bot(command_prefix='!', description=discordDescription)

#Set up PRAW instance
reddit = praw.Reddit('bot1',
                     client_id=     PRAWclientId,
                     client_secret= PRAWclientSecret,
                     username=      PRAWusername,
                     password=      PRAWpassword,
                     user_agent=    PRAWuserAgent)

#Confirm bot is logged in
@bot.event
async def on_ready():
    print('Logged in to Discord as')
    print('-----' + bot.user.name + '-----')
    print('-----' + bot.user.id + '-----')
    print('---------------------------')

#Methods used in bot commands
def getRandomPostFromReddit(subVar):
    sub = reddit.subreddit(subVar)
    picker = randint(0, 99)
    postList = []
    print('---------------Fetching top 100 posts on r/' + subVar + '---------------')
    for submission in sub.hot(limit=100):
        postList.append(submission.url)
    print('Randomly selected post:'+ ' ' + picker + ' ' + postList[picker])
    return postList[picker]

#TODO
@bot.command(pass_context=True)
async def mystats(ctx):
    try:
        await bot.say(getStats(ctx.message.author.name))
    except:
        await bot.say("This feature is under construction.")
#TODO
@bot.command(pass_context=True)
async def top3(ctx):
    try:
        await bot.say(getTop3())
    except:
        await bot.say("This feature is under construction")
#TODO
def getStats(user):
    userstats = db.stats.find({'users' : user})
    for hit in userstats:
        print(hit)
    return userstats
#TODO
def getTop3():
    pass

#Bot commands
@bot.command(pass_context=True)
async def hmmm(ctx):
    await bot.say(getRandomPostFromReddit('hmmm'))
    author = ctx.message.author.name
    event = {'user' : author,
             'sub' : 'hmmm'}
    try:
       result = db.stats.insert_one(event)
    except:
        print("DB operation failed")

@bot.command(pass_context=True)
async def wtf(ctx):
    await bot.say(getRandomPostFromReddit('wtf'))
    author = ctx.message.author.name
    event = {'user' : author,
             'sub' : 'wtf'}
    try:
        result = db.stats.insert_one(event)
    except:
        print("DB operation failed")

@bot.command(pass_context=True)
async def gif(ctx):
    await bot.say(getRandomPostFromReddit('gifs'))
    author = ctx.message.author.name
    event = {'user' : author,
             'sub' : 'gifs'}
    try:
        result = db.stats.insert_one(event)
    except:
        print("DB operation failed")

#Run Main
if __name__ == '__main__':
    try: 
        bot.run(discordToken)
    except:
        print("Error conntecting to Discord server")