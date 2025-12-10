from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from random import randint


class GridManager():

    def __init__(self, size: int):
        if size %3 !=0:
            raise Exception('Invalid grid size , size should be a multiple of 3')
        if size <3:
            raise Exception('Size must be greater than 3')
        self.size = size
        self.data = [[None for _ in range(size)] for _ in range(size)]

    def addObject(self, wall: Wall,player1_hive: Hive, player2_hive: Hive,player3_hive: Hive, player4_hive: Hive) -> list[list]:
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):

                # Set walls around the border
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    self.data[r][c] = wall

                # add the hives on the map
                if r == 1 and c == 1:
                    self.data[r][c] = player1_hive
                if r == 1 and c == cols - 2:
                    self.data[r][c] = player2_hive
                if r == rows-2 and c == 1:
                    self.data[r][c] = player3_hive
                if r == rows-2 and c == cols - 2:
                    self.data[r][c] = player4_hive

        return self.data

    def spawnFlower(self, flower: Flower, numberFlower: int) -> list[list]:
        rows = len(self.data)
        cols = len(self.data[0])

        chunk = cols // 3
        middle_line = rows // 2

        possible_cells = []

        for r in range(rows):
            for c in range(cols):

                if r <= 1: #out of bound safety
                    continue

                if r != 0 and c != 0 and c != rows - 1:
                    if chunk - 1 < c < cols - chunk and r < middle_line and c < middle_line:
                        possible_cells.append((r, c))
                    if chunk < r < middle_line and c < middle_line:
                        possible_cells.append((r, c))


        if numberFlower %2 != 0:
            raise Exception('numberFlower should be a multiple of 2')

        for _ in range(numberFlower //2):
            i = randint(0, len(possible_cells)-1)
            flower_row , flower_col = possible_cells.pop(i)
            self.data[flower_row][flower_col] = flower

            mirrored_row = 2 * middle_line - flower_row
            self.data[mirrored_row][flower_col] = flower
            mirrored_col = 2 * middle_line - flower_col
            self.data[flower_row][mirrored_col] = flower
            self.data[mirrored_row][mirrored_col] = flower

            r
            #print(middle_line-flower_row)


        return self.data


    def render(self):
        for row in self.data:
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    line += str(cell.displayObject) + " "
            print(line)
