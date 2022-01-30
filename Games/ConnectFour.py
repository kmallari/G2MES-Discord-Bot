class ConnectFour:
    def __init__(self):
        self.ROW = 6
        self.COL = 7

        # game.grid = [   [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0]   ]

        self.grid = [[0 for row in range(self.COL)] for i in range(self.ROW)]

        self.current_turn = 1
        self.winner_found = False

    def check_win(self):

        # check rows
        for row in range(self.ROW):
            left = 0
            right = self.COL - 3
            for cell in range(self.COL - 3):
                # print(self.grid[row][left:right])
                if (
                    self.grid[row][left:right].count(1) == 4
                    or self.grid[row][left:right].count(-1) == 4
                ):
                    print("ROW WIN")
                    return self.grid[row][left]
                right += 1
                left += 1

        # check columns
        for row in range(self.ROW - 3):
            for cell in range(self.COL):
                temp = [
                    self.grid[row + i][cell]
                    for i in range(4)
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
                    self.grid[row + i][cell + i]
                    for i in range(4)
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
                    self.grid[row + i][cell - i]
                    for i in range(4)
                    if self.grid[row][cell] != 0
                ]
                # print(temp)
                if temp.count(1) == 4 or temp.count(-1) == 4:
                    print("TR->BL WIN")
                    return temp[0]

        # check for draw
        num_of_zeros = 0
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    num_of_zeros += 1
            if num_of_zeros != 0:
                break

        if num_of_zeros == 0:
            return "draw"

        return 0

    def make_turn(self, symbol, column):
        symbol = int(symbol)
        column = int(column) - 1
        if not self.winner_found and self.current_turn == int(symbol):
            # ADD CODE TO CHECK IF COL IS FULL
            if column < self.COL:
                for row in range(self.ROW):
                    if row == 0 and self.grid[row][column] != 0:
                        return "full"
                    if row == self.ROW - 1 or (
                        self.grid[row + 1][column] != 0 and self.grid[row][column] == 0
                    ):
                        self.grid[row][column] = symbol
                        break
                self.current_turn *= -1
            # print(self.grid)
            return True
        elif self.current_turn != symbol:
            return False

    # testing functitons
    def info(self):
        print("grid", self.grid)
        print("coordinates", self.coordinates)
