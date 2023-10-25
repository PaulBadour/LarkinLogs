import discord # Discord.py
from dotenv import load_dotenv # python-dotenv
import os
from GetStats import getPlayerPoints

dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(dir, 'token.env'))
dtok = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)




@bot.event

async def on_ready():
    print("Ready")



@bot.event

async def on_message(message):
    date = "10/24/23"
    command = message.content.lower().split(' ')
    if command[0] == ".points":
        if len(command) == 1:
            await message.channel.send(f"{message.author.mention} you didnt give me a player retard")
        
        stats = getPlayerPoints(date)
        if command[1] in stats.keys():
            name = command[1]

        elif len(command) == 3 and (' '.join(command[1:3]) in stats.keys() or ' '.join(command[1:3]) == 'red wings'):
            name = ' '.join(command[1:3])

        else:
            await message.channel.send(f"{message.author.mention} they did not play in this game faggot")
            return
        points = stats[name]
        if name in ('wings', 'red wings'):
            await message.channel.send(f"{message.author.mention} the Wings earned {points} point{'' if points == 1 else 's'}")
        else:
            await message.channel.send(f"{message.author.mention} that bitch {name} got {points} point{'' if points == 1 else 's'}")
bot.run(dtok)