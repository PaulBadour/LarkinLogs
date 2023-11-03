import discord # Discord.py
from dotenv import load_dotenv # python-dotenv
import os
from GetStats import getPlayerPoints
import SheetInteract

dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(dir, 'token.env'))
dtok = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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
            await message.channel.send(f"{message.author.mention} they did not play in this game retard")
            return
        points = stats[name]
        if name in ('wings', 'red wings'):
            await message.channel.send(f"{message.author.mention} the Wings earned {points} point{'' if points == 1 else 's'}")
        else:
            await message.channel.send(f"{message.author.mention} that bitch {name} got {points} point{'' if points == 1 else 's'}")

    elif command[0] == ".admin" and command[1] == 'addstats':
        print('adding stats')
        s = SheetInteract.Sheet()
        stats,drafted = s.addPointStats(command[2])
        del s
        string = f"@everyone Points for {command[2]} are in!\nPoint Scorers:\n"
        for i in stats.keys():
            if stats[i] != 0:
                string += f"{i.capitalize()}: {stats[i]} point{'s' if stats[i] != 1 else ''} {'Unclaimed' if len([j[0] for j in drafted if i == j[1] or i == j[2]])==0 else 'for ' + [j[0] for j in drafted if i == j[1] or i == j[2]][0]}"
        await message.channel.send(string)

    elif command[0] == ".admin" and command[1] == 'setupgame':
        print('setting up game')
        s = SheetInteract.Sheet()
        firstPick = s.setupGame(command[2])
        await message.channel.send(content=f"@everyone The Draft for {command[2]} has started!", allowed_mentions=discord.AllowedMentions(everyone = True))
        await message.channel.send(f"<@{nameToID(firstPick)}> you have first overall pick!")
        del s

    elif command[0] == ".pick":
        s = SheetInteract.Sheet()
        pick = s.getNextDraftee()
        if pick == None:
            await message.channel.send(f"{message.author.mention} no active draft retard")
            return
        if int(nameToID(pick)) != message.author.id:
            await message.channel.send(f"{message.author.mention} its not your pick retard")
            return
        res = s.pickPlayer(command[1])
        if res:
            await message.channel.send(f"Player drafted. <@{nameToID(s.getNextDraftee())}> has next pick")
        elif res == False:
            await message.channel.send(f"<@{nameToID(s.getNextDraftee())}> player has already been drafted")

        else:
            await message.channel.send(f"Player drafted. Draft is over!")
        del s

def nameToID(name):
    d = {'Eddy': '333328782092009472', 'Paul': '297418880811401226', 'Flynn': '344874985971515403', 'Johnson': '217693320447655936'}
    return d[name]

def IDToName(id):
    d = {v : k for k, v in {'Eddy': '333328782092009472', 'Paul': '297418880811401226', 'Flynn': '344874985971515403', 'Johnson': '217693320447655936'}.items()}
    return d[id]

bot.run(dtok)