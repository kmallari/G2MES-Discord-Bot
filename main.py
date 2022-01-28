# Notes:
#     - Games:
#         * Tic Tac Toe
#         * Connect 4
#         * Hangman
#         * Obstruction (https://www.artofmanliness.com/living/games-tricks/5-pencil-and-paper-games-that-arent-tic-tac-toe/)
#         * UNO (?)

PREFIX = "+"

from discord.ext import commands
# from discord.utils import get
import discord
import os
# from replit import db # allows access to replit database
import random
import string

# bot and client startup
client = discord.Client()
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

challenger_dict = {}  # challenged: challenger

# will be used to check if a player is already in game
players = {}

rooms = {}


def generate_room(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# @client.command(name='create', help="Créer un salon privé")
@commands.has_permissions(manage_channels=True, manage_roles=True)
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="GAME5"))


# challenge player command
@bot.command()
async def c(ctx):
    if (ctx.message.mentions[0].id == ctx.author.id):
        await ctx.channel.send("You cannot send a challenge to yourself!")
    else:
        challenger_dict[ctx.message.mentions[0]] = ctx.author
        await ctx.channel.send(
            f"""Player <@{ctx.message.mentions[0].id}> has been challenged!
Type the command ``{PREFIX}a`` to accept the challenge, or ``{PREFIX}r`` to reject the challenge."""
        )


# accept challenge from most recent challenger
@bot.command()
async def a(ctx):
    # checks if author has been challenged
    if ctx.author in challenger_dict.keys():
        category_name = "GAME5 Rooms"
        # await ctx.send("Setting up management!")
        category = discord.utils.get(ctx.guild.categories, name=category_name)
        user = ctx.author
        overwrites = {
            ctx.guild.default_role:
            discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me:
            discord.PermissionOverwrite(read_messages=True),
            ctx.author:
            discord.PermissionOverwrite(read_messages=True),
            challenger_dict[ctx.author]:
            discord.PermissionOverwrite(read_messages=True)
        }

        if category is None:  #If there's no category matching with the `name`
            # creates a new category
            category = await ctx.guild.create_category(category_name,
                                                       overwrites=None,
                                                       reason=None)
            channel_name = generate_room(6)
            await ctx.guild.create_text_channel(channel_name,
                                                overwrites=overwrites,
                                                reason=None,
                                                category=category)

        else:  #Else if it found the categoty
            # await ctx.guild.create_text_channel(user,
            #                                     overwrites=overwrites,
            #                                     reason=None,
            #                                     category=category)
            channel_name = generate_room(6)
            await ctx.guild.create_text_channel(channel_name,
                                                overwrites=overwrites,
                                                reason=None,
                                                category=category)

        # adds the two users to the players dict and deletes
        # them from the challenger dict

        players[ctx.author] = challenger_dict[ctx.author]
        rooms[channel_name] = {
            "players": [ctx.author, challenger_dict[ctx.author]]
        }
        del challenger_dict[ctx.author]
    else:
        await ctx.channel.send("You have not been challenged.")


@bot.command()
async def r(ctx):
    if ctx.author in challenger_dict.keys():
        await ctx.channel.send(
            f"You have rejected <@{challenger_dict[ctx.author].id}>'s challenge."
        )
        del challenger_dict[ctx.author]
    else:
        await ctx.channel.send("You have not been challenged.")


# // --------------- //


@bot.command()
async def p(ctx):
    print(challenger_dict)


@bot.command()
async def chall_info(ctx):
    print(challenger_dict)


@bot.command()
async def cat_test(ctx):
    if ctx.message.channel.name in rooms:
        print(True)
    else:
        print(False)


@bot.command()
async def chan(ctx):
    print(type(ctx.message.channel))
    print(ctx.message.channel)
    print(type(ctx.message.channel.name))
    print(ctx.message.channel.name)


@bot.command()
async def r_info(ctx):
    print(rooms)


bot.run(os.getenv('TOKEN'))
