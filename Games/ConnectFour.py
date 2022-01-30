class ConnectFour():
    def __init__(self, player_one_id, player_two_id):
        self.ROW = 6
        self.COL = 7

        # game.grid = [   [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0]   ]

        self.grid = [[0 for row in range(self.COL)] for i in range(self.ROW)]

        self.player_one = player_one_id
        self.player_two = player_two_id

        self.previous_turn = -1

        self.coordinates = {}
        self.temp_i = 1

        for i in range(self.ROW):
            for j in range(self.COL):
                self.coordinates[f"{self.temp_i}"] = [i, j]
                self.temp_i += 1

        self.winner_found = False

    def check_win(self):

        # check rows
        for row in range(self.ROW):
            left = 0
            right = self.COL - 3
            for cell in range(self.COL - 3):
                # print(self.grid[row][left:right])
                if self.grid[row][left:right].count(
                        1) == 4 or self.grid[row][left:right].count(-1) == 4:
                    print("ROW WIN")
                    return self.grid[row][left]
                right += 1
                left += 1

        # check columns
        for row in range(self.ROW - 3):
            for cell in range(self.COL):
                temp = [
                    self.grid[row + i][cell] for i in range(4)
                    if self.grid[row][cell] != 0
                ]
                # print(temp)
                if temp.count(1) == 4 or temp.count(-1) == 4:
                    print("COL WIN")
                    return temp[0]

        # check diagonals
        # top left to bottom right
        for row in range(self.ROW - 3):
            # temp = []
            for cell in range(self.COL - 3):
                temp = [
                    self.grid[row + i][cell + i] for i in range(4)
                    if self.grid[row][cell] != 0
                ]
                # print(temp)
                if temp.count(1) == 4 or temp.count(-1) == 4:
                    print("TL->BR WIN")
                    return temp[0]

        # check top right to bottom left
        for row in range(self.ROW - 3):
            for cell in range(3, self.COL):
                temp = [
                    self.grid[row + i][cell - i] for i in range(4)
                    if self.grid[row][cell] != 0
                ]
                # print(temp)
                if temp.count(1) == 4 or temp.count(-1) == 4:
                    print("TR->BL WIN")
                    return temp[0]

        return 0

    def make_turn(self, symbol, column):
        if column < self.COL:
            for row in range(self.ROW):
                if row == self.ROW-1 or (self.grid[row+1][column] != 0 and self.grid[row][column] == 0):
                    self.grid[row][column] = symbol

    # testing functitons
    def info(self):
        print("grid", self.grid)
        print("coordinates", self.coordinates)
