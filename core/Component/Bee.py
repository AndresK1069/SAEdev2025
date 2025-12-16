
from core.Player import Player
from core.Component import Hive
from data.constante import TIME_KO

class Bee(object):
    def __init__(self, beeHealth ,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str ,simpleMovement :bool, currentNectar: int , stunCounter :int , moveList : list , isStun : bool, currenthealth: int ):
        self.beeHealth = beeHealth
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        self.simpleMovement = simpleMovement
        self.currentNectar = currentNectar
        self.stunCounter = stunCounter
        self.moveList = moveList
        self.isStun = isStun
        self.currenthealth = currenthealth

    def checkOverFlow(self) -> None:
        if self.currentNectar > self.maxNectar:
            self.currentNectar = self.maxNectar

    def stun(self):
        self.currenthealth=self.beeHealth
        self.currentNectar =0
        self.stunCounter =TIME_KO
        self.isStun = True




