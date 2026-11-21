import discord, random
from discord.ext import commands
from bot_logic import gen_pass, gen_emodji, flip_coin
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def passgen(ctx, pass_length = 10):
    await ctx.send(gen_pass(pass_length))

@bot.command()
async def emoji(ctx):
    await ctx.send(gen_emodji())

@bot.command()
async def coin(ctx):
    await ctx.send(flip_coin())

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

def get_tips(how_many):
    tips_for_teen = [
        "Cobalah untuk menghindari penggunaan barang sekali pakai, seperti gelas dan botol plastik",
        "Pindah ke e-reader untuk mengurangi konsumsi kertas",
        "Pilih produk bahan makanan dan makanan ringan dengan kemasan sesedikit mungkin, beli makanan berdasarkan beratnya (tanpa kemasan), dan cobalah beralih ke tas yang dapat digunakan kembali",

    ]

    return random.sample(tips_for_teen, k=how_many)

@bot.command('tipsteen')
async def tipsteen(ctx, howmany:int=2):
    all_tips = get_tips(howmany)
    sent_tips = '\n'.join(all_tips)
    await ctx.send(sent_tips)

def get_waste_type(waste):
    #standarisasi inputan
    waste = waste.lower().strip()
    non_recyclable_waste = ["food scraps", "dirty tissue", "diaper", "cigarette butt", "styrofoam"]
    recyclable_waste = ["plastic bottle", "plastic cup", "glass bottle", "newspaper", "cardboard", "can"]

    if waste in recyclable_waste:
        return "It's a recyclable waste"
    elif waste in non_recyclable_waste:
        return "Non recyclable waste" 
    else:
        return "Not found"

@bot.command('type')
async def waste_type(ctx, *, waste:str):
    type_waste = get_waste_type(waste)

    await ctx.send(type_waste)
