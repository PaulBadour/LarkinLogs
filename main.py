import discord # Discord.py
from dotenv import load_dotenv # python-dotenv
import os


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

    if message.content == "yo":
        await message.channel.send("Hey retard")


bot.run(dtok)