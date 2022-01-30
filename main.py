# Notes:
#     - Games:
#         * Tic Tac Toe
#         * Connect 4
#         * Hangman
#         * Obstruction (https://www.artofmanliness.com/living/games-tricks/5-pencil-and-paper-games-that-arent-tic-tac-toe/)
#         * UNO (?)

#  TO FIX
# CHECK IF TTT DRAW WORKS, IF A SQUARE HAS BEEN TAKEN, IT CANNOT BE CHANGED FOR TTT

PREFIX = "+"

from discord.ext import commands

# from discord.utils import get
import discord
import os
# from replit import db # allows access to replit database
import random
import string
from Games.TicTacToe import TicTacToe

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


def ttt_board(game):

    number_emoji_equivalent = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }

    curr_cell = 1
    display_grid = ""

    for i, row in enumerate(game.grid):
        for j, cell in enumerate(row):
            if cell == 0:
                display_grid += number_emoji_equivalent[curr_cell]
            else:
                if cell == 1:
                    display_grid += "❎"
                elif cell == -1:
                    display_grid += "🅾"

            curr_cell += 1
        display_grid += "\n"

    return display_grid


def c4_board(game):
    pass


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
            # "players": [ctx.author, challenger_dict[ctx.author]],
            "players": {
                f"{ctx.author.id}": {
                    "symbol": ""
                },
                f"{challenger_dict[ctx.author].id}": {
                    "symbol": ""
                }
            },
            "turn": 1,
            "ongoing_game": ""
        }
        del challenger_dict[ctx.author]
    else:
        await ctx.channel.send("You have not been challenged.")


@bot.command()
async def r(ctx):
    if ctx.author.id in challenger_dict.keys():
        await ctx.channel.send(
            f"You have rejected <@{challenger_dict[ctx.author].id}>'s challenge."
        )
        del challenger_dict[ctx.author.id]
    else:
        await ctx.channel.send("You have not been challenged.")


@bot.command()
async def ttt(ctx, msg):
    channel_name = ctx.message.channel.name
    if msg == "start":
        if channel_name in rooms:

            rooms[channel_name]["ongoing_game"] = TicTacToe()
            game = rooms[channel_name]["ongoing_game"]

            room_players = list(rooms[channel_name]["players"].keys())
            # print(room_players)
            # print(rooms[channel_name]["players"][str(room_players[0])])

            p1_symbol = random.choice([1, -1])
            p2_symbol = p1_symbol * -1

            rooms[channel_name]["players"][str(room_players[0])]["symbol"] = p1_symbol
            rooms[channel_name]["players"][str(room_players[1])]["symbol"] = p2_symbol

            if rooms[channel_name]["players"][room_players[0]]["symbol"] == 1:
                await ctx.channel.send(f"""Randomly choosing who goes first...
<@{room_players[0]}>, you will go first with the ❎ symbol! <@{room_players[1]}>, you will go second with the 🅾

Type the command ``+ttt <number>`` with the number being the square you want to put your symbol in to make a move."""
                                       )
            else:
                await ctx.channel.send(f"""Randomly choosing who goes first...
<@{room_players[1]}>, you will go first with the ❎ symbol! <@{room_players[0]}>, you will go second with the 🅾 symbol!>

Type the command ``+ttt <number>`` with the number being the square you want to put your symbol in to make a move."""
                                       )

            # game_grid = ttt_board(rooms[channel_name]["ongoing_game"])
            await ctx.channel.send(ttt_board(game))
        else:
            await ctx.channel.send("You are not in a GAME5 Room!")

    elif int(msg) >= 1 and int(msg) <= 9:
        game = rooms[channel_name]["ongoing_game"]
        player_symbol = rooms[channel_name]["players"][str(ctx.author.id)]["symbol"]
        make_turn = game.make_turn(player_symbol, msg)
        if make_turn == True:
            rooms[channel_name]["turn"] *= -1
            await ctx.channel.send(ttt_board(game))
            if game.check_win() == 1 or game.check_win() == -1:
                await ctx.channel.send(f"<@{ctx.author.id}> wins!")
                rooms[channel_name]["ongoing_game"] = ""
            elif game.check_win() == "draw":
                await ctx.channel.send(f"It's a draw!")
                rooms[channel_name]["ongoing_game"] = ""
        elif make_turn == False:
            await ctx.channel.send("It is not your turn!")
        elif make_turn == "taken":
            await ctx.channel.send("Someone has already chosen that square!")


# // --------------- //


@bot.command()
async def p(ctx):
    print(players)


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


@bot.command()
async def test_ttt(ctx):
    game = TicTacToe(1, 2)
    game.grid = [
        [1, 0, -1],
        [0, 0, 1],
        [-1, 1, 0],
    ]
    game_grid = ttt_board(game)
    await ctx.channel.send(game_grid)


@bot.command()
async def test_msg(ctx, msg):
    await ctx.channel.send(msg)


@bot.command()
async def del_rooms(ctx):
    category = bot.get_channel(int(936456804332863508))

    for channel in category.text_channels:
        await channel.delete()

    print("Deleted game rooms.")

@bot.command()
async def game_info(ctx):
    channel_name = ctx.message.channel.name
    print(rooms[channel_name]["ongoing_game"].__dict__)

bot.run(os.getenv('TOKEN'))
