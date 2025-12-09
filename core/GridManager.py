from core.Component.Wall import Wall
from core.Component.Hive import Hive
from core.Component.Flower import Flower


class GridManager():

    def __init__(self, size: int):
        self.size = size
        self.data = [[None for _ in range(size)] for _ in range(size)]

    # TODO Bonus automatique grid gen
    def addObject(self, wall: Wall, flower: Flower,player1_hive: Hive, player2_hive: Hive,player3_hive: Hive, player4_hive: Hive) -> list[list]:
        """
        Adds garnish elements around the grid.
        """
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

    def render(self):
        for row in self.data:
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    line += str(cell.displayObject) + " "
            print(line)
