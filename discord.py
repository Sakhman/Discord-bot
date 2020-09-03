import discord
from discord.utils import get
import random



class MyClient(discord.Client):
    #Einloggen
    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Game('$help'))
        print('Ich habe mich eingeloggt. beep bop.')

    #Wenn Nachricht gepostet wird
    async def on_message(self, message):
        if message.author == client.user:
            return


        if message.content.startswith('$social'):
            await message.channel.send('https://linktr.ee/mptvfn')


        if message.content.startswith('$help'):
            await message.channel.send('Ich habe sie dir per DM Nachricht gesendet!!!')
            await message.author.send('Commands: $roulette [red, black, eine Zahl von 0 bis 36] | $social')


        if message.content.startswith('$roulette '):
            bid = message.content.split(' ')[1]
            bid_param = -3
            if bid.lower() == 'black':
                bid_param = -1
            elif bid.lower() == 'red':
                bid_param = -2
            else:
                try:
                    bid_param = int(bid)
                except:
                    bid_param = -3
            if bid_param == -3:
                await message.channel.send('Ungültige Eingabe')
                return
            result = random.randint(0,36)
            if bid_param == -1:
                won = result%2 == 0 and not result == 0
            elif bid_param == -2:
                won = result%2 == 1
            else:
                won = result == bid_param
            if won:
                await message.channel.send('$$$ Du hast gewonnen!!! $$$')
            else:
                await message.channel.send('Leider verloren:(')


            if message.context.startswith('$play'):
                where = message.content.split(' ')[1]
                channel = get(message.guild.channels, name=where)
                voicechannel = await channel.connect()
                voicechannel.play(discord.FFmpegPCMAudio('lol.mp3'))


client = MyClient()
client.run('NzQzMjMxMjcyNzM3OTY0MDYz.XzRqDw.T5FRTMHafMrH79rKMC4IPklc8lw')