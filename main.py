import re, flask, os, asyncio, random, string, keep_alive, discord
from discord.ext import commands, tasks

version = '1.0'

bot_prefix = "-"

user_token = "MTAwNTY2MzcxMTEyMzQ5MzAyNQ.GBLpCw.TkrEU95icKRlW1zGmyQyEtcR6ksMz6fQgrohxc" 
spam_id = 1245321402232602694
WHITELISTED_SERVERS = [1007105952434094121] #put your server id in [] and delete previous one
BLACKLISTED_CHANNELS = [1120191562060660777]  
ping_id = ""
user_id = ""

intervals = [3, 3, 3, 3] 


try:
    ping_id = os.environ['ping_id']
except:
    ping_id = False
try:
    user_id = os.environ['user_id']
except:
    user_id = False
sh_interval = False

with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('data/legendary', 'r') as file:
    legendary_list = file.read()
with open('data/mythical', 'r') as file:
    mythical_list = file.read()
with open('data/level', 'r') as file:
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



@spam.before_loop
async def before_spam():
    await bot.wait_until_ready()


spam.start()


@bot.event
async def on_ready():
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
                        await asyncio.sleep(3)  #Hint Delay, ffs not do 1
                        await message.channel.send('<@716390085896962058> h')
                    elif "Congratulations" in embed_title:
                        embed_content = message.embeds[0].description
                        if 'now level' in embed_content:
                            split = embed_content.split(' ')
                            a = embed_content.count(' ')
                            level = int(split[a].replace('!', ''))
                            if level == 100:
                                await message.channel.send(f"{mention} s {to_level}")
                                with open('data/level', 'r') as fi:
                                    data = fi.read().splitlines(True)
                                with open('data/level', 'w') as fo:
                                    fo.writelines(data[1:])
                else:
                    content = message.content
                    if 'The pokémon is ' in content:
                        if not len(solve(content)):
                            print('Pokemon not found.')
                        else:
                            for i in solve(content):
                                await asyncio.sleep(2)  #Catch Delay
                                await message.channel.send(
                                    f'<@716390085896962058> c {i}')
                        check = random.randint(1, 60)
                        if check == 1:
                            await asyncio.sleep(900)
                            spam.start()
                        else:
                            await asyncio.sleep(1)
                            spam.start()

                    elif 'Congratulations' in content:
                        global shiny
                        global legendary
                        global num_pokemon
                        global mythical
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!', '')
                        if 'seem unusual...' in content:
                            shiny += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'    ⭐ A SHINY Pokémon was caught! ⭐')
                            print('ㅤㅤㅤㅤ')
                            print(f'    - Total Pokémon Caught: {num_pokemon}')
                            print(f'    - Mythical Pokémon Caught: {mythical}')
                            print(
                                f'    - Legendary Pokémon Caught: {legendary}')
                            print(f'    - Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            

                        elif re.findall('^' + pokemon + '$', legendary_list,
                                        re.MULTILINE):
                            legendary += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     💎 A LEGENDARY Pokémon was caught! 💎')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     - Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     - Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     - Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     - Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            

                        elif re.findall('^' + pokemon + '$', mythical_list,
                                        re.MULTILINE):
                            mythical += 1

                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     💥 A MYTHICAL Pokémon was caught! 💥')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     - Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     - Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     - Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     - Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')

                            
                            print('ㅤㅤㅤㅤ')
                            print(
                                '-----------------------------------------------'
                            )
                            print(f'     A new Pokémon was caught!')
                            print('ㅤㅤㅤㅤ')
                            print(
                                f'     - Total Pokémon Caught: {num_pokemon}')
                            print(
                                f'     - Mythical Pokémon Caught: {mythical}')
                            print(
                                f'     - Legendary Pokémon Caught: {legendary}'
                            )
                            print(f'     - Shiny Pokémon Caught: {shiny}')
                            print(
                                '-----------------------------------------------'
                            )
                            print('ㅤㅤㅤㅤ')


                    elif 'human' in content:
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
async def say(ctx, *, arg):
   if ctx.author.id == user_id:
        return
   try:
        await ctx.send(f'{arg}')

   except:
        await ctx.send('nthg')
    
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
keep_alive.keep_alive()
bot.run(f"{user_token}")
