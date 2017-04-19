class Tile:

    def __init__(self):
        self.char = None

    def set_char(self, char):
        self.char = char

    def get_char(self):
        return self.char

ROW_SIZE = 8
COL_SIZE = 8

grid = [[j for j in range(ROW_SIZE)] for i in range(COL_SIZE)]

for m in range(8):
    for n in range(8):
        print(grid[m][n], end=" ")
    print("")

char = 65
for k in range(8):
    for l in range(8):
        grid[k][l] = Tile()
        grid[k][l].set_char(chr(char))
        char += 1
    print("")

print("==============")
#
#print(grid[0][0].get_i())

print("==============")

for m in range(8):
    for n in range(8):
        print(grid[m][n].get_char(), end=": ")
    print("")

