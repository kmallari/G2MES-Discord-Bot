class TicTacToe():
    def __init__(self):
        self.GRID_SIZE = 3

        #[
        #   [0, 0, 0],
        #   [0, 0, 0],
        #   [0, 0, 0],
        #]

        self.grid = [[0 for row in range(self.GRID_SIZE)]
                     for i in range(self.GRID_SIZE)]
                     
        # self.player_one = player_one_id
        # self.player_two = player_two_id

        self.coordinates = {}
        self.temp_i = 1

        self.current_turn = 1

        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.coordinates[f"{self.temp_i}"] = [i, j]
                self.temp_i += 1

        self.winner_found = False

    def check_win(self):
        if not self.winner_found:
            # check rows
            for row in self.grid:
                if row.count(1) == len(row) or row.count(-1) == len(row):
                    self.winner_found = True
                    return row[0]  # returns the value of winner (either 1 or -1)

            # check columns
            for i in range(self.GRID_SIZE):
                temp_col = [self.grid[j][i] for j in range(self.GRID_SIZE)]
                # for j in range(self.GRID_SIZE):
                #     temp_col.append(self.grid[j][i])
                if temp_col.count(1) == len(row) or temp_col.count(-1) == len(row):
                    self.winner_found = True
                    return self.grid[i][0]
                    # returns the value of winner (either 1 or -1)

            # checks diagonals
            if (self.grid[1][1] == self.grid[0][0] == self.grid[2][2]) or (
                    self.grid[1][1] == self.grid[0][2] == self.grid[2][0]):
                self.winner_found = True
                return self.grid[1][1]
                # returns the middle cell, which is also the winner

        return 0

    def make_turn(self, symbol, cell):
        if not self.winner_found and self.current_turn == symbol:
            # print(self.coordinates[cell][0], self.coordinates[cell][1])
            self.grid[self.coordinates[cell][0]][self.coordinates[cell][1]] = symbol
            print(self.check_win())
            self.current_turn *= -1
            return True
        elif self.current_turn != symbol:
            return False

    # testing functions
    def check_coords(self):
        print(self.coordinates)

    def print_grid(self):
        print(self.grid)
        