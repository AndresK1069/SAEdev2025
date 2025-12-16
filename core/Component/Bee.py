
from core.Player import Player
from core.Component import Hive

class Bee(object):
    def __init__(self, beeHealth ,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str ,simpleMovement :bool, currentNectar: int , stunCounter :int , moveList : list ):
        self.beeHealth = beeHealth
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        self.simpleMovement = simpleMovement
        self.currentNectar = currentNectar
        self.stunCounter = stunCounter
        self.moveList = moveList

    def checkOverFlow(self) -> None:
        #TODO add a more refine way to check for over flow
        if self.currentNectar > self.maxNectar:
            self.currentNectar = self.maxNectar



