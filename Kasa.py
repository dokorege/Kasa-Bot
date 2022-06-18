import asyncio
from asyncio.events import get_event_loop
from discord.ext import commands, tasks 
import discord
from discord import message
import random
import string
import requests

def quotes():
 
   response = requests.get('https://animechan.vercel.app/api/random')
   json_data = response.json()
   quote =   'From: ' + json_data["anime"] + ', '  + json_data["character"] + ': ' + '"' + json_data["quote"] + '"'
   return quote 

def kitty():
 
   response = requests.get('https://cataas.com/cat?json=true%27')
   json_data = response.json()
   cat = json_data['url']
   cat1 = 'https://cataas.com/' + cat
   return cat1

def dog():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    json_data = response.json()
    doggy = str(json_data['message'])
    return(doggy)

def fox():
    response = requests.get('https://randomfox.ca/floof/')
    json_data = response.json()
    foxxy = str(json_data['image'])
    return(foxxy)

def waifu_choices():
    return f'SFW Categories:\n***Waifu Neko Shinobu Megumin\nBully Cuddle Cry Hug\nAwoo Kiss Lick Pat\nSmug Bonk Yeet Blush\nSmile Wave High Five\nHandhold Nom Bite Glomp\nSlap Kill Kick Happy\nWink Poke Dance Cringe***\n\nNSFW Choices:\n***Waifu Trap Neko Blowjob ***'

class MyClient(discord.Client):
    
    async def on_ready(self):
        print(self.user)
        print(self.user.id)
    
    async def on_message(self, message):
        # Self == Bot, without self == user 

        if message.content.startswith('!fox'):
            await message.channel.send(fox())

        if message.content.startswith('!dog'):
            await message.channel.send(dog())

        if message.content.startswith('!cat'):
            await message.channel.send(kitty())

        if message.content.startswith('!anime_quote'):
            await message.channel.send(quotes())

     # -----------------------------------------------------------------------------------------------------------------

        async def dice_roll():
            # Prevents bot from responding to itself
            if message.author.id == self.user.id:
                return
            # This will make sure that the response will only be registered if the following conditions are met:
            async def check(ctx):
                return ctx.author == message.author and ctx.content.isdigit()
            answer = random.randint(1, 10)
            try:
                # Essnetially User Input
                msg = await client.wait_for('message', check=check, timeout=5)
                
            except asyncio.TimeoutError:
                return await message.channel.send(f'Waited to Long, it was {answer}')
            finally:
                if int(msg.content) == answer:
                    await message.channel.send('Correct!')
                else:
                    await message.channel.send(f'Wrong! It was actually {answer}')
        
        if message.content.startswith('!dice'):
            await message.channel.send(f'Pick a Number Between 1-10: ')
            await dice_roll()

    # -----------------------------------------------------------------------------------------------------------------

        def passGenerator():
            passContents = []
            Points = ['!', '.']
            lenDetermine = random.randint(1,3)
            gen = 0
            while gen <= lenDetermine:

                gen += 1 
                passContents.append(random.choice(string.ascii_lowercase))
                passContents.append(random.choice(string.ascii_uppercase))
                passContents.append(random.choice(string.digits))
                passContents.append(random.choice(random.choice(Points)))
            
            return "".join(passContents)
            
        async def password_gen():
            if message.author.id == self.user.id:
                return

            if message.author.id != self.user.id:
                await message.channel.send(passGenerator())
        
        if message.content.startswith('!pass'):
            await password_gen()

    # -----------------------------------------------------------------------------------------------------------------

        async def rps():
            if message.author.id == self.user.id:
                return

            CHOICES = ['SCISSORS', 'ROCK', 'PAPER']
            BOT_RESPONSE = random.choice(CHOICES)
            print(BOT_RESPONSE)
            
            try:
                user_input = await client.wait_for('message', timeout=10)
            except asyncio.TimeoutError:
                await message.channel.send(f'Took To Long To Respond! I Chose {BOT_RESPONSE.lower()}.')
            finally:
                
                if user_input.content.upper() in CHOICES: 
                    
                    if user_input.content.upper() == BOT_RESPONSE:
                        await message.channel.send(f"It's a tie! We both chose {BOT_RESPONSE.lower()}.")
                        return
                        
                    if user_input.content.upper() == 'SCISSORS':
                        if BOT_RESPONSE == 'PAPER':
                            await message.channel.send(f'You Won! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}.')
                            return
                        if BOT_RESPONSE == 'ROCK':
                            await message.channel.send(f'You Lost! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}.')
                            return
                    
                    if user_input.content.upper() == 'PAPER':
                        if BOT_RESPONSE == 'ROCK':
                            await message.channel.send(f'You Won! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}.')
                            return
                        if BOT_RESPONSE == 'SCISSORS':
                            await message.channel.send(f'You Lost! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}')
                            return

                    if user_input.content.upper() == 'ROCK':
                        if BOT_RESPONSE == 'SCISSORS':
                            await message.channel.send(f'You Won! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}.')
                        if BOT_RESPONSE == 'PAPER':
                            await message.channel.send(f'You Lost! I chose {BOT_RESPONSE.lower()}, you chose {user_input.content.lower()}')
                            return
                else:
                    await message.channel.send('Not In Choice List, Run Command Again')    
                    return
        
        if message.content.startswith('!rps'):
                await message.channel.send(f'Choose Rock, Paper, or Scissors: ')
                await rps()
    # -----------------------------------------------------------------------------------------------------------------

        async def dictonary_api():

            try:
                user_input = await client.wait_for('message', timeout=10)
            except asyncio.TimeoutError:
                    await message.channel.send(f'Took To Long To Respond!')

            data = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{user_input.content}')
            json_data = data.json()
            try:
                definition = json_data[0]['meanings'][0]['definitions'][0]['definition']
                await message.channel.send(definition)
            except:
                await message.channel.send(json_data['title'])

        if message.content.startswith('!search'):
            await message.channel.send('What word would you want to search?: ')
            await dictonary_api()

    # -----------------------------------------------------------------------------------------------------------------

        async def waifu_nsfw():
            
            try:
                user_input = await client.wait_for('message', timeout=15)
            except asyncio.TimeoutError:
                await message.channel.send(f'Took To Long To Respond!')
            
            response = requests.get(f'https://api.waifu.pics/nsfw/{user_input.content.lower()}')
            json_data = response.json()
            
            try:
                waifuu = str(json_data["url"])
            except:
                await message.channel.send(json_data['message'] + '. Choose from !waifu_choices for all possible requests.')
            finally:
                await message.channel.send(waifuu)
        
        async def waifu():
            
            try:
                user_input = await client.wait_for('message', timeout=15)
            except asyncio.TimeoutError:
                await message.channel.send(f'Took To Long To Respond!')
            
            response = requests.get(f'https://api.waifu.pics/sfw/{user_input.content.lower()}')
            json_data = response.json()
            
            try:
                waifuu = str(json_data["url"])
            except:
                await message.channel.send(json_data['message'] + '. Choose from !waifu_choices for all possible requests.')
            finally:
                await message.channel.send(waifuu)
        
        if message.content.startswith('!nsfw'):
            await message.channel.send('Use !choices for all possible Tags!\nPlease Enter A Tag: ')
            await waifu_nsfw()

        if message.content.startswith('!waifu'):
            await message.channel.send('Use !choices for all possible Tags!\nPlease Enter A Tag: ')
            await waifu()
        
        if message.content.startswith('!choices'):
            await message.channel.send(waifu_choices())
    # -----------------------------------------------------------------------------------------------------------------



client = MyClient()
client.run('Bot Token')
