from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from random import randint
import copy


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

        coord_hive = []

        for r in range(rows):
            for c in range(cols):

                # Set walls around the border
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    self.data[r][c] = wall

                # add the hives on the map
                if r == 1 and c == 1:
                    self.data[r][c] = player1_hive
                    coord_hive.append((r,c))
                if r == 1 and c == cols - 2:
                    self.data[r][c] = player2_hive
                    coord_hive.append((r, c))
                if r == rows-2 and c == 1:
                    self.data[r][c] = player3_hive
                    coord_hive.append((r, c))
                if r == rows-2 and c == cols - 2:
                    self.data[r][c] = player4_hive
                    coord_hive.append((r, c))

        return self.data , coord_hive

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

            #print(middle_line-flower_row)


        return self.data

    def cellToList(self, row: int, col: int) -> list:
        varObject = self.data[row][col]
        return [copy.copy(varObject)]

    def cleanGrid(self):
        #Scan the canva and remove list with only the hive inside
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], list) and len(self.data[r][c]) ==  1:
                    for hive in self.data[r][c]:
                        hive_ = hive
                    self.data[r][c] = hive_


        return

    def moveObject(self , bee ,nRow :int, nCol :int) -> None:
        #TODO bee can't go in adversary camp
        from core.Component.Bee import Bee
        if isinstance(bee, Bee):

            rows = len(self.data)
            cols = len(self.data[0])

            if nRow >= rows:
                raise Exception('nRow should be smaller than rows')
            if nCol >= cols:
                raise Exception('nCol should be smaller than cols')

            for r in range(rows):
                for c in range(cols):

                    if isinstance(self.data[r][c], list) and bee in self.data[r][c]:
                        if bee.simpleMovement:
                            if nCol != c and nRow != r:
                                raise Exception("Diagonal movement is not allowed")

                            if nRow > r + bee.beeAgility :
                                raise Exception('nCol and nRow should be smaller than rows')
                            if nCol > c + bee.beeAgility :
                                raise Exception('nCol and nRow should be smaller than cols')

                            if self.data[nRow][nCol] is None:
                                self.data[nRow][nCol] = bee

                                self.data[r][c].remove(bee)
                        else:
                            if not bee.simpleMovement:

                                if nRow > r + bee.beeAgility:
                                    raise Exception('nCol and nRow should be smaller than rows')
                                if nCol > c + bee.beeAgility:
                                    raise Exception('nCol and nRow should be smaller than cols')

                                if self.data[nRow][nCol] is None:
                                    self.data[nRow][nCol] = bee

                                    self.data[r][c].remove(bee)

                    #TODO remove this duplicate code
                    else:
                        if self.data[r][c] is bee:
                            if bee.simpleMovement:
                                if nCol != c and nRow != r:
                                    raise Exception("Diagonal movement is not allowed")

                                if nRow > r + bee.beeAgility:
                                    raise Exception('nCol and nRow should be smaller than rows')
                                if nCol > c + bee.beeAgility:
                                    raise Exception('nCol and nRow should be smaller than cols')

                                if self.data[nRow][nCol] is None:
                                    self.data[nRow][nCol] = bee

                                    self.data[r][c] = None
                                else:
                                    if not bee.simpleMovement:

                                        if nRow > r + bee.beeAgility:
                                            raise Exception('nCol and nRow should be smaller than rows')
                                        if nCol > c + bee.beeAgility:
                                            raise Exception('nCol and nRow should be smaller than cols')

                                        if self.data[nRow][nCol] is None:
                                            self.data[nRow][nCol] = bee

                                            self.data[r][c] = None

        return self.data


    def recupFleur(self) -> list[(int ,int)]:
        flower_array = []
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Flower):
                    flower_array.append((r, c))
        return flower_array

    def flowerButinage(self, arrFlower:list) -> None:
        from core.Component.Bee import Bee
        for f in arrFlower:
            r,c = f
            row , col = f
            r-=1
            c-=1
            #print(r,c)
            for col in range(3):
                for row in range(3):
                    if isinstance(self.data[r+row][c+col], Bee):
                        #TODO finish butinage logic
                        print("BEE IN BUTINAGE AREA")


    def emptyBeeNectar(self ,arrayhive:list) -> None:
        from core.Component.Bee import Bee
        for f in arrayhive:
            r, c = f
            row_, row_ = f
            r -= 1
            c -= 1
            # print(r,c)
            for col in range(3):
                for row in range(3):
                    if isinstance(self.data[r + row][c + col], Bee):
                        nectarStock = self.data[r + row][c + col].currentNectar
                        self.data[row_][row_].currentNectar += nectarStock
                        self.data[r + row][c + col].currentNectar -= nectarStock


    def render(self)->None:
        for row in self.data:
            line = ""
            for cell in row:

                #Change with render priority system
                if isinstance(cell,list):
                    line += "L "
                    continue

                if cell is None:
                    line += ". "
                else:
                    line += str(cell.displayObject) + " "
            print(line)
