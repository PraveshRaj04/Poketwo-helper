import aiosqlite 
from discord.ext import commands,tasks
from keep_alive import keep_alive
import os, json, re, asyncio, random
import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
import aiohttp, ast 

version = '4.6'

bot_prefix = "-69"

token = "MTI0NTM4ODQ5NjE4OTkxOTI0Mg.G2kvqB.HKQFwTQ79BU8erxriUDUj6jAmJn3u_wCJlAWHw" 
spam_id = 1245391014739447919
WHITELISTED_SERVERS = [1237999659553656864, 1245390164654686208 , 1245388990329393354, 1245390263237738496, 1245390376093745272 , 1245390443819040788, 1245390517051854969] #put your server id in [] and delete previous one
BLACKLISTED_CHANNELS = [1120191562060660777]  
ping_id = 1245391048964837467
user_id = "1005663711123493025"

intervals = [3, 2, 3, 2] 



sh_interval = False

with open('pokemon.txt', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('legendary.txt', 'r') as file:
    legendary_list = file.read()
with open('mythical.txt', 'r') as file:
    mythical_list = file.read()
with open('level.txt', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058  #Pokétwo's ID
mention = f'<@{poketwo}>'

bot = commands.Bot(command_prefix=bot_prefix)
stopped = False
verified = True
loaded_model = load_model('model.h5', compile=False)
with open('classes.json', 'r') as f:
    classes = json.load(f)

def solve(message):
    if not stopped:
        hint = []
        for i in range(15, len(message) - 1):
            if message[i] != '\\':
                hint.append(message[i])
        hint_string = ''
        for i in hint:
            hint_string += i
        hint_replaced = hint_string.replace('_', '.')
        solution = re.findall('^' + hint_replaced + '$', pokemon_list,
                              re.MULTILINE)
        return solution


@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = bot.get_channel(int(spam_id))
    await channel.send(''.join(
        random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 7) *
        5))




@bot.event
async def on_ready():
    spam.start()
    print(f'Logged into account: {bot.user.name}')


@bot.event
async def on_message(message):
    global stopped
    global verified
    if ping_id:
        ping__channel = bot.get_channel(int(ping_id))
    if message.guild.id in WHITELISTED_SERVERS and message.channel.id not in BLACKLISTED_CHANNELS:
        if message.author.id == poketwo:
            if not stopped:
                if message.embeds:
                    embed_title = message.embeds[0].title
                    if 'wild pokémon has appeared!' in embed_title and not stopped:
                        spam.cancel()
                        await asyncio.sleep(0)  #Hint Delay, ffs not do 1
                        if message.embeds[0].image:
                           url = message.embeds[0].image.url
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url=url) as resp:
                            if resp.status == 200:
                                content = await resp.read()
                                image_data = BytesIO(content)
                                image = Image.open(image_data)
                    preprocessed_image = await preprocess_image(image)
                    predictions = loaded_model.predict(preprocessed_image)
                    classes_x = np.argmax(predictions, axis=1)
                    name = list(classes.keys())[classes_x[0]]
                    async with message.channel.typing():
                        await asyncio.sleep(0)
                    await message.channel.send(
                        f'<@716390085896962058> c {name} ')
                    spam.start()
                elif "wrong" in message.content:
                  async with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.channel.send(f'{mention}h')
                elif  'The pokémon is ' in message.content:
                        if not len(solve(message.content)):
                            print('Pokemon not found.')
                        else:
                            for i in solve(message.content):
                                  #Catch Delay
                                await message.channel.send(
                                    f'<@716390085896962058> c {i}')
                        check = random.randint(1, 60)
                        if check == 1:
                            await asyncio.sleep(900)
                            spam.start()
                        else:
                            await asyncio.sleep(1)
                            spam.start()

                    


                elif 'human' in message.content:
                    spam.cancel()
                    if ping_id:
                            await ping__channel.send(
                                f" **__Captcha detected!__**\nYour autocatcher has been paused because of a  pending captcha. Please verify from the below link and use the command {bot_prefix}captcha to continue."
                            )
                            if user_id:
                                await ping__channel.send(
                                    f'Captcha Ping: <@{user_id}>\nhttps://verify.poketwo.net/captcha/{bot.user.id}')

                            print(
                                f"Captcha has been detected! Please use =verified in discord to reactivate the autocatcher!"
                            )
                            spam.cancel()
                            stopped = True
                            verified = False
    if not message.author.bot:
        await bot.process_commands(message)



@bot.command()
async def stop(ctx):
    if verified:
        global stopped
        await ctx.send(
            f"<:level30:1113344800272416818> The autocatcher has been paused. Please use {bot_prefix}start to resume the autocatcher."
        )
        spam.cancel()
        stopped = True
    else:
        await ctx.send(
            f"<:level30:1113344800272416818> You can not stop the autocatcher while there's a pending captcha! Use {bot_prefix}verified instead."
        )

async def preprocess_image(image):
    image = image.resize((64, 64))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@bot.command()
async def start(ctx):
    if verified:
        global stopped
        await ctx.send(
            f"<:level30:1113344800272416818> The autocatcher has been started. Use {bot_prefix}stop to stop the autocatcher."
        )
        spam.start()
        stopped = False
    else:
        await ctx.send(
            f"<:level30:1113344800272416818> You can't start the autocatcher while there's a pending captcha! Use {bot_prefix}verified instead."
        )


@bot.command()
async def verified(ctx):
    global verified
    global stopped
    if verified == True:
        await ctx.send("<:level30:1113344800272416818> There aren't any pending captchas!")

    else:
        await ctx.send(
            "<:level30:1113344800272416818> Captcha confirmed! Autocatcher has been reactivated!")
        stopped = False
        spam.start()
        verified = True




#say command below  
@bot.command()
async def say(ctx, *, args):
    await ctx.send(f'{args}')
    
@bot.command(aliases = ['t'])
async def trade(ctx, *, args):
    await ctx.send(f'{mention} t {args}')

@bot.command(aliases = ['s'])
async def sayy(ctx, *, args):
    await ctx.send(f'{mention} {args}')
 
@bot.command(name = 'balance', aliases = ['bal'])
async def balance(ctx):
    await ctx.send(f'{mention} bal')

@bot.command(name = 'quests', aliases = ['q'])
async def quests(ctx):
    await ctx.send(f'{mention} q')

@bot.command(name = 'shiny', aliases = ['sh'])
async def shiny(ctx):
    await ctx.send(f'{mention} p --sh')

@bot.command(name = 'event', aliases = ['ev'])
async def event(ctx):
    await ctx.send(f'{mention} p --ev')

@bot.command(aliases = ['m'])
async def market(ctx, *, args):
    await ctx.send(f'{mention} m b {args}')
      
      
print(
    f'Pokétwo Autocatcher {version}\nA free and open-source Pokétwo autocatcher made by GiLL\nEvent Log:'
)

keep_alive()
bot.run(f"{token}")
