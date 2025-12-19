from core.Player import Player
from core.Component.Bees.BeeTypes import BEE_TYPES

class Hive(object):
    def __init__(self, displayObject: str , owner: Player, beeList :list , maxNectar :int , currentNectar :int ,baseList:list):
        self.displayObject = displayObject
        self.owner = owner
        self.beeList = beeList
        self.maxNectar = maxNectar
        self.currentNectar = currentNectar
        self.baseList = baseList

    def spawnBee(self, beeType: str):
        beeType_ = beeType.lower()
        if beeType_ not in BEE_TYPES:
            raise ValueError("Invalid beeType")

        bee_class = BEE_TYPES[beeType_]
        bee = bee_class()
        self.beeList.append(bee)
        return bee

