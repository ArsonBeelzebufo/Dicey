import os
import discord
import dotenv
import random
import json
import ast

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FOUNDING_FATHERS=os.getenv("FOUNDING_FATHERS").split(',')
MEMES_CHANNELS=ast.literal_eval(os.getenv("MEMES_CHANNELS"))
MEMES_ADDRESSES=ast.literal_eval(os.getenv("MEMES_ADDRESSES"))
dicey=discord.Client(intents=discord.Intents.all())
go=True
dupedict={}
if input("Clear logs? (y/n) ")=="y":
    log=open("log.csv",'w').close()
with open("format.json",'r') as file:
    format=json.load(file)

def getaddress(content,key):
    content+=" "
    idx=content.index(key)+len(key)
    address=""
    start,end=False,False
    while not start:
        if content[idx]==" " and content[idx+1]!=" ":
            start=True
        idx+=1
    while not end:
        address+=content[idx]
        idx+=1
        if content[idx]==" ":
            end=True
    return address
def logify(content):
    out='"'
    for i in content:
        if i=='"':
            out+='""'
        elif i=='\n':
            out+='\\n'
        else:
            out+=i
    return out+'"'

@dicey.event
async def on_ready():
    print(f"{dicey.user} has connected to Discord!")
@dicey.event
async def on_message(message):
    global go
    content=message.content.lower()
    formes=f"{message.guild},{message.guild.id},{message.channel},{message.channel.id},{message.author},{message.author.id},{logify(message.content)}"
    print(formes)
    with open("log.csv",'a',encoding="utf-8") as log:
        log.write(formes+'\n')
    if str(message.author.id) in FOUNDING_FATHERS and f"<@{dicey.user.id}>" in message.content:
        #big authorized commands
        if "stop" in message.content.lower():
            go=False
            await message.channel.send(random.choice(format["stop"]))
        if "jesusify" in message.content.lower():
            go=True
            await message.channel.send(random.choice(format["jesusify"]))
        if "kys" in message.content.lower():
            await message.channel.send(random.choice(format["kys"]))
            await dicey.close()
        if "meme" in content:
            if "address" in content:
                try:
                    address=getaddress(content,"address")
                except:
                    dupedict[message.channel.id]=True
                    await message.channel.send("put the address after \"address\" dumbass")
                    return
                if "unlink" in content:
                    if address not in MEMES_CHANNELS:
                        dupedict[message.channel.id]=True
                        await message.channel.send("this address doesnt exist bro")
                        return
                    if message.channel.id not in MEMES_CHANNELS[address]:
                        dupedict[message.channel.id]=True
                        await message.channel.send("already unlinked")
                    else:
                        MEMES_CHANNELS[address].remove(message.channel.id)
                        MEMES_ADDRESSES[message.channel.id].remove(address)
                        dupedict[message.channel.id]=True
                        await message.channel.send(f"unlinked from address {address}")
                elif "delink" in content:
                    if address not in MEMES_CHANNELS:
                        dupedict[message.channel.id]=True
                        await message.channel.send("this address doesnt exist bro")
                        return
                    for channel in MEMES_CHANNELS[address]:
                        MEMES_ADDRESSES[channel].remove(address)
                    del MEMES_CHANNELS[address]
                    dupedict[message.channel.id]=True
                    await message.channel.send(f"address {address} deleted")
                else:
                    if "new" in content:
                        if address in MEMES_CHANNELS:
                            dupedict[message.channel.id]=True
                            await message.channel.send("you didnt check the address list did you")
                        else:
                            MEMES_CHANNELS[address]=[]
                            dupedict[message.channel.id]=True
                            await message.channel.send(f"new address created at {address}")
                    if "link" in content:
                        if address not in MEMES_CHANNELS:
                            dupedict[message.channel.id]=True
                            await message.channel.send("this address doenst exist bro")
                            return
                        if message.channel.id in MEMES_CHANNELS[address]:
                            dupedict[message.channel.id]=True
                            await message.channel.send("already linked to this address")
                        else:
                            MEMES_CHANNELS[address].append(message.channel.id)
                            if message.channel.id not in MEMES_ADDRESSES:
                                MEMES_ADDRESSES[message.channel.id]=[]
                            MEMES_ADDRESSES[message.channel.id].append(address)
                            dupedict[message.channel.id]=True
                            await message.channel.send(f"this channel linked to address {address}")
                dotenv.set_key(".env","MEMES_CHANNELS",str(MEMES_CHANNELS))
                dotenv.set_key(".env","MEMES_ADDRESSES",str(MEMES_ADDRESSES))
            if "list" in content:
                if "here" in content:
                    dupedict[message.channel.id]=True
                    await message.channel.send("channel under addresses:\n"+'\n'.join(MEMES_ADDRESSES[message.channel.id]))
                if "channels" in content:
                    try:
                        address=getaddress(content,"channels")
                    except:
                        dupedict[message.channel.id]=True
                        await message.channel.send("missing address")
                        return
                    dupedict[message.channel.id]=True
                    await message.channel.send(f"channels under address {address}:\n"+'\n'.join([str(i) for i in MEMES_CHANNELS[address]]))
                if "all" in content:
                    dupedict[message.channel.id]=True
                    await message.channel.send("addresses:\n"+'\n'.join(MEMES_CHANNELS))
            return
    if str(message.author.id) in FOUNDING_FATHERS and "dicey" in message.content.lower():
        #smaller authorized commands
        pass
    if go:
        if message.channel.id in MEMES_ADDRESSES:
            if message.author==dicey.user:
                try:
                    if dupedict[message.channel.id]:
                        del dupedict[message.channel.id]
                        return
                except:
                    pass
            for address in MEMES_ADDRESSES[message.channel.id]:
                for channel in MEMES_CHANNELS[address]:
                    if channel!=message.channel.id:
                        dupedict[channel]=True
                        await dicey.get_channel(channel).send(content=message.content,files=[await i.to_file() for i in message.attachments])
        if sum([i in message.content.lower() for i in ["tiger","woods","golf","club"]])>0:
            if message.author!=dicey.user:
                order=[0,1,2] #hi, i'm tiger woods, nice to meet you
                random.shuffle(order)
                presence=[bool(random.getrandbits(1)) for i in range(2)] #hi, nice to meet you
                presence.insert(order.index(1),True)
                await message.channel.send(" ".join([presence[i]*random.choice(format["tiger"][order[i]]) for i in range(3)]))

dicey.run(TOKEN)