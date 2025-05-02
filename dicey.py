import os
import discord
import dotenv
import random

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FOUNDING_FATHERS=os.getenv("FOUNDING_FATHERS").split(',')
dicey=discord.Client(intents=discord.Intents.all())
go=True
if input("Clear logs? (y/n) ")=="y":
    log=open("log.csv",'w').close()

@dicey.event
async def on_ready():
    print(f"{dicey.user} has connected to Discord!\n")
@dicey.event
async def on_message(message):
    global go
    formes=f"{message.guild},{message.guild.id},{message.channel},{message.channel.id},{message.author},{message.author.id},{message.content}\n"
    print(formes)
    with open("log.csv",'a') as log:
        log.write(formes)
    if message.author==dicey.user:
        return
    if str(message.author.id) in FOUNDING_FATHERS and f"<@{dicey.user.id}>" in message.content:
        #big authorized commands
        if "kys" in message.content.lower():
            go=False
            await message.channel.send(random.choice(["fuck you","i love you too","ok lil bro"]))
        if "jesusify" in message.content.lower():
            go=True
            await message.channel.send(random.choice(["i have risen"]))
    if str(message.author.id) in FOUNDING_FATHERS and "dicey" in message.content.lower():
        #smaller authorized commands
        pass
    if go:
        if sum([i in message.content.lower() for i in ["tiger","woods","golf","club"]])>0:
            order=[0,1,2] #hi, i'm tiger woods, nice to meet you
            random.shuffle(order)
            presence=[bool(random.getrandbits(1)) for i in range(2)] #hi, nice to meet you
            presence.insert(order.index(1),True)
            components=[["hi","hey","hello"],["i'm tiger woods","tiger woods"],["nice to meet you","nice meeting you"]]
            await message.channel.send(" ".join([presence[i]*random.choice(components[order[i]]) for i in range(3)]))

dicey.run(TOKEN)