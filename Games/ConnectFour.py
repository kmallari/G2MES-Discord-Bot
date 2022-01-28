class ConnectFour():
    def __init__(self, player_one_id, player_two_id):
        self.ROW = 6
        self.COL = 7
        self.grid = [[0 for row in range(self.COL)] for i in range(self.ROW)]

        self.player_one = player_one_id
        self.player_two = player_two_id

        self.coordinates = {}
        self.temp_i = 1

        for i in range(self.ROW):
            for j in range(self.COL):
                self.coordinates[f"{self.temp_i}"] = [i, j]
                self.temp_i += 1

        self.winner_found = False

    def check_win(self):

        #  IMPROVE LOGIC TO BASE THE CHECK OFF OF THE LAST MOVE
        # MADE TO MAKE THE CHECK SPEED FASTER
        
        # check rows
        for row in range(self.ROW):
            left = 0
            right = self.COL - 4 + 1
            for cell in range(self.COL - 4 + 1):
                # print(self.grid[row][left:right])
                if self.grid[row][left:right].count(
                        1) == 4 or self.grid[row][left:right].count(-1) == 4:
                    print("ROW WIN")
                    return self.grid[row][left]
                right += 1
                left += 1

        #check columns
        for row in range(self.ROW - 4 + 1):
            for cell in range(self.COL):
                temp = [
                    self.grid[row + i][cell] for i in range(4)
                    if self.grid[row][cell] != 0
                ]
                if temp.count(1) == 4 or temp.count(-1) == 4:
                    print("COL WIN")
                    return temp[0]

        return 0

    # testing functitons
    def info(self):
        print("grid", self.grid)
        print("coordinates", self.coordinates)
