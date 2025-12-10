
from core.Player import Player
from core.Component import Hive

class Bee(object):

    def __init__(self, beeHealth ,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str ,simpleMovement :bool):
        self.beeHealth = beeHealth
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        self.simpleMovement = simpleMovement

