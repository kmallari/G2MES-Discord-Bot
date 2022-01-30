from Games.TicTacToe import TicTacToe
from Games.ConnectFour import ConnectFour

game = ConnectFour(1, 2)

game.make_turn(1, 5)
game.make_turn(1, 5)
game.make_turn(1, 5)
game.make_turn(1, 5)

game.info()
print(game.check_win())

game.grid = [   [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]   ]

# game.grid = [   [0, 0, 0, 0, 0, 0, 0],
#                 [0, 0, 0, 0, 0, 0, 0],
#                 [0, 0, 0, 0, 0, 0, 0],
#                 [0, 0, 0, 0, 0, 0, 0],
#                 [0, 0, 0, 0, 0, 0, 0],
#                 [0, 0, 0, 0, 0, 0, 0]   ]


# game.info()

test = [1 , 1, 1, 0]

if (test[0] == test[1] == test[2] != 1):
    print("TEST")