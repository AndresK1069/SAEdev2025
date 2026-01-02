from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from random import randint
from data.constante import MAX_NECTAR
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


    def getBattleZone(self, wall) -> list[list]:
        rows = len(self.data)
        cols = len(self.data[0])

        chunk = cols // 3
        middle_line = rows // 2

        for r in range(rows):
            for c in range(cols):
                if chunk - 1 < c < cols - chunk:
                    self.data[r][c] = wall
                if chunk -1 < r < cols-chunk  :
                    self.data[r][c] = wall
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

    def is_valid_cell(self, bee, r:int, c:int, nRow:int, nCol:int) -> bool:
        rows = len(self.data)
        cols = len(self.data[0])

        if nRow < 0 or nRow >= rows or nCol < 0 or nCol >= cols:
            raise Exception("Target cell out of bounds")


        if self.data[nRow][nCol] is not None:
            raise Exception("Target cell is not empty")

        row_diff = abs(nRow - r)
        col_diff = abs(nCol - c)

        if bee.simpleMovement:
            if row_diff > 0 and col_diff > 0:
                raise Exception("Diagonal movement is not allowed")


            if row_diff > bee.beeAgility or col_diff > bee.beeAgility:
                raise Exception("Move exceeds agility")

        else:
            if max(row_diff, col_diff) > bee.beeAgility:
                raise Exception("Move exceeds agility")

        return True

    def moveObject(self, bee, nRow: int, nCol: int) -> None:
        from core.Component.Bee import Bee

        if not isinstance(bee, Bee):
            return self.data

        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):

                cell = self.data[r][c]

                # bee inside a list
                if isinstance(cell, list) and bee in cell:
                    self.is_valid_cell(bee, r, c, nRow, nCol)

                    self.data[nRow][nCol] = bee
                    cell.remove(bee)
                    return self.data

                if cell is bee:
                    self.is_valid_cell(bee, r, c, nRow, nCol)

                    self.data[nRow][nCol] = bee
                    self.data[r][c] = None
                    return self.data

        raise Exception("Bee not found in matrix")


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
            reel_row , reel_col = f
            r-=1
            c-=1
            for col in range(3):
                for row in range(3):
                    if isinstance(self.data[r+row][c+col], Bee):
                        move1, move2 = self.data[r+row][c+col].moveList[-2:]
                        if move1 == move2:
                            #print(self.data[reel_row][reel_col].flowerNectar)
                            varNectar = self.data[reel_row][reel_col].reduceNectar()
                            self.data[r+row][c+col].currentNectar += varNectar
                            self.data[r + row][c + col].checkOverFlow()



    def getBeePos(self) -> None:
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Bee):
                    self.data[r][c].moveList.append((r,c))

    def emptyBeeNectar(self, arrayhive: list) -> None:
        from core.Component.Bee import Bee

        for f in arrayhive:
            r, c = f  # coordonnées de la hive
            # row_ et col_ inutiles ici
            for col_offset in range(3):
                for row_offset in range(3):
                    nr = r + row_offset
                    nc = c + col_offset

                    # sécurité sur les limites de la grille
                    if 0 <= nr < len(self.data) and 0 <= nc < len(self.data[0]):
                        cell = self.data[nr][nc]
                        if isinstance(cell, Bee):
                            nectarStock = cell.currentNectar
                            print(type(self.data[r][c]))
                            self.data[r][c].currentNectar += nectarStock
                            cell.currentNectar = 0

    def checkEscarmouche(self) -> None:
        from core.Component.Bee import Bee
        print("checking for Escarmouche ... ")
        rows = len(self.data)
        cols = len(self.data[0])

        for r in range(rows):
            for c in range(cols):
                bee = self.data[r][c]
                if isinstance(bee, Bee):
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr = r + dr
                            nc = c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                neighbor = self.data[nr][nc]
                                if (nr, nc) == (r, c):
                                    continue

                                if isinstance(neighbor, Bee):
                                    if bee.owner != neighbor.owner:
                                        #TODO ADD PROPER BATTLE
                                        print(f"found escarmouche between ({r},{c}) and ({nr},{nc})")
                                        neighbor.beeHealth -= bee.beeStrength

    def checkBeeHealth(self) -> None:
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Bee):
                    if self.data[r][c].beeHealth <= 0:
                        self.data[r][c].stun()
                if isinstance(self.data[r][c], Bee) and self.data[r][c].isStun:
                    self.data[r][c].stunCounter-=1
                if isinstance(self.data[r][c], Bee) and self.data[r][c].isStun:
                    if self.data[r][c].stunCounter <= 0:
                        self.data[r][c].isStun = False

    def getFlowerNectar(self) -> int:
        nectar = 0
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Flower):
                    nectar +=  self.data[r][c].flowerNectar
        return nectar

    def getBeeNectar(self) -> int:
        nectar = 0
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], Bee):
                    nectar += self.data[r][c].currentNectar
        return nectar

    def isWinner(self, arrayhive: list):
        won = False
        winning_hive_row = 0
        winning_hive_col = 0

        for x in arrayhive:
            if isinstance(x, list):
                hive = next((y for y in x if isinstance(y, Hive)), None)
                if hive is None:
                    continue
                r, c = getattr(hive, "row", None), getattr(hive, "col", None)
                if r is None or c is None:
                    continue
                if hive.currentNectar >= MAX_NECTAR:
                    won = True
                    winning_hive_row = r
                    winning_hive_col = c
                    break
            else:
                r, c = x
                cell = self.data[r][c]
                if hasattr(cell, "currentNectar") and cell.currentNectar >= MAX_NECTAR:
                    won = True
                    winning_hive_row = r
                    winning_hive_col = c
                    break

        return won, winning_hive_row, winning_hive_col

    def maxNectar(self, arrayhive: list) -> tuple[int, int]:
        max_nectar = 0
        winning_hive_row = 0
        winning_hive_col = 0

        for x in arrayhive:
            if isinstance(x, list):
                hive = next((y for y in x if isinstance(y, Hive)), None)
                if hive is None:
                    continue
                if hive.currentNectar > max_nectar:
                    max_nectar = hive.currentNectar
                    idx = arrayhive.index(x)
                    r, c = arrayhive[idx] if not isinstance(arrayhive[idx], list) else (0, 0)
                    winning_hive_row = r
                    winning_hive_col = c
            else:
                r, c = x
                cell = self.data[r][c]
                if hasattr(cell, "currentNectar") and cell.currentNectar > max_nectar:
                    max_nectar = cell.currentNectar
                    winning_hive_row = r
                    winning_hive_col = c

        return winning_hive_row, winning_hive_col

    def setSafeZoner(self):
        # TODO create safe zone
        pass




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
