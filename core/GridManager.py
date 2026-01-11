from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from random import randint, random

from core.utilities import evenSplit
from data.constante import MAX_NECTAR, NFLEURS
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

    def spawnFlower(self, numberFlower: int) -> list[list]:
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

        for _ in range(numberFlower):
            i = randint(0, len(possible_cells)-1)
            flower_row , flower_col = possible_cells.pop(i)
            self.data[flower_row][flower_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))

            mirrored_row = 2 * middle_line - flower_row
            self.data[mirrored_row][flower_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))
            mirrored_col = 2 * middle_line - flower_col
            self.data[flower_row][mirrored_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))
            self.data[mirrored_row][mirrored_col] = Flower("f",evenSplit(NFLEURS,MAX_NECTAR))

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

    def is_valid_cell(self, bee, r: int, c: int, nRow: int, nCol: int) -> bool:
        rows = len(self.data)
        cols = len(self.data[0])

        # Check bounds
        if nRow < 0 or nRow >= rows or nCol < 0 or nCol >= cols:
            raise Exception("Target cell out of bounds")

        # Check if target is empty
        if self.data[nRow][nCol] is not None:
            raise Exception("Target cell is not empty")

        row_diff = nRow - r
        col_diff = nCol - c

        if bee.simpleMovement:
            # Only horizontal or vertical moves
            if row_diff != 0 and col_diff != 0:
                raise Exception("Diagonal movement is not allowed")
        if abs(row_diff) > bee.beeAgility or abs(col_diff) > bee.beeAgility:
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
            r, c = f
            reel_row, reel_col = r, c
            r -= 1
            c -= 1
            for row in range(3):
                for col in range(3):
                    obj = self.data[r + row][c + col]
                    if isinstance(obj, Bee):
                        if len(obj.moveList) == 1:
                            continue
                        move1, move2 = obj.moveList[-2:]
                        if move1 == move2:
                            varNectar = self.data[reel_row][reel_col].reduceNectar()
                            obj.currentNectar += varNectar
                            obj.checkOverFlow()

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
        print(arrayhive)
        for r, c in arrayhive:
            hive = self.data[r][c]
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < len(self.data) and 0 <= nc < len(self.data[0]):
                        cell = self.data[nr][nc]
                        if isinstance(cell, Bee) and cell.currentNectar > 0:
                            hive.addNectar(cell.currentNectar)
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
                                        if not neighbor.isStun:

                                            print(f"found escarmouche between ({bee.name}) and ({neighbor.name})")
                                            numEnemy =self.getBeeAround(r,c)
                                            dodgeProba = self.calFE(r ,c , numEnemy)
                                            FE = bee.beeStrength // numEnemy
                                            didDamege = self.did_dodge(dodgeProba)
                                            if not didDamege:
                                                neighbor.currenthealth -= FE
                                                if neighbor.currenthealth <= 0:
                                                    neighbor.stun()

    def did_dodge(self,dodgeProba: int) -> bool:
        return random() < dodgeProba / 100

    def getBeeAround(self, r, c) -> int:
        from core.Component.Bee import Bee
        """
        Count the number of enemy Bee objects surrounding the cell at (r, c).
        This method checks the 8 neighboring cells (including diagonals) around
        the given position. Only Bee instances with a different owner than the
        Bee at (r, c) are counted. If the cell at (r, c) does not contain a Bee,
        the method returns 0.
    
        Parameters
        ----------
        r : int
            Row index of the center cell.
        c : int
            Column index of the center cell.
    
        Returns
        -------
        int
            The number of surrounding enemy Bees.
        """
        beeNum = 0

        if not isinstance(self.data[r][c], Bee):
            return 0

        rows = len(self.data)
        cols = len(self.data[0])
        center_bee = self.data[r][c]

        for dr in range(r - 1, r + 2):
            for dc in range(c - 1, c + 2):
                if dr < 0 or dr >= rows or dc < 0 or dc >= cols:
                    continue
                if dr == r and dc == c:
                    continue

                cell = self.data[dr][dc]
                if isinstance(cell, Bee) and cell.owner != center_bee.owner:
                    beeNum += 1

        return beeNum

    def calFE(self,r :int,c :int, beeNum:int)-> int:
        from core.Component.Bee import Bee
        sumBeeStrenght = 0

        if not isinstance(self.data[r][c], Bee):
            return 0

        rows = len(self.data)
        cols = len(self.data[0])
        center_bee = self.data[r][c]

        for dr in range(r - 1, r + 2):
            for dc in range(c - 1, c + 2):
                if dr < 0 or dr >= rows or dc < 0 or dc >= cols:
                    continue
                if dr == r and dc == c:
                    continue

                cell = self.data[dr][dc]
                if isinstance(cell, Bee) and cell.owner != center_bee.owner:
                    sumBeeStrenght+= cell.beeStrength
        return sumBeeStrenght // beeNum


    def checkStunBee(self) -> None:
        from core.Component.Bee import Bee
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                cell = self.data[r][c]
                if isinstance(cell, Bee) and cell.isStun:
                    print("Current count:", cell.stunCounter)
                    if cell.stunCounter <= 0:
                        cell.isStun = False
                        continue
                    print("Before:", cell.stunCounter)
                    cell.stunCounter -= 1
                    print("After:", cell.stunCounter)



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
                if hasattr(cell, "currentNectar") and cell.currentNectar >= MAX_NECTAR or cell.currentNectar >= MAX_NECTAR//2:
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

    def getItemCoord(self,x):
        rows = len(self.data)
        cols = len(self.data[0])
        for r in range(rows):
            for c in range(cols):
                if isinstance(self.data[r][c], list):
                    for item in self.data[r][c]:
                        if id(item) == id(x):
                            return r, c

                if id(self.data[r][c]) == id(x):
                    return (r, c)

    def setSafeZone(self, hive_array:list) -> None:
        if len(hive_array) != 4:
            raise ValueError("Expected at least 4 hives")
        tmpSize=self.size
        chunk = tmpSize//3
        zones = [
            ((0, chunk), (0, chunk)),
            ((0, chunk), (chunk * 2, tmpSize)),
            ((chunk * 2, tmpSize), (0, chunk)),
            ((chunk * 2, tmpSize), (chunk * 2, tmpSize))
        ]
        for hive , zones in zip(hive_array, zones):
            hive.baseList.append( (hive.owner, zones) )

    def getAreaOwner(self, hive_list: list, r: int, c: int) -> str | None:
        for hive in hive_list:
            for owner, ((r1, r2), (c1, c2)) in hive.baseList:
                if r1 <= r < r2 and c1 <= c < c2:
                    return owner
        return None


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
