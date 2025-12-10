from core.Player import Player
from core.Component.Bees.BeeTypes import BEE_TYPES

class Hive(object):
    def __init__(self, displayObject: str , owner: Player, beeList :list):
        self.displayObject = displayObject
        self.owner = owner
        self.beeList = beeList

    def spawnBee(self ,grid :list[list[None]] , coord:list , beeType: str):
        beeType_ = beeType.lower()
        if beeType_ not in BEE_TYPES:
            raise ValueError("Invalid beeType")

        row, col = coord
        print(row, col)
        #check surrounding cell to check if cell is pawning is possible

        pass
