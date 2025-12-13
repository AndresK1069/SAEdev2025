
from core.Player import Player
from core.Component import Hive

class Bee(object):

    #TODO add propre nectar cost field
    #TODO add current nectar field

    def __init__(self, beeHealth ,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str ,simpleMovement :bool):
        self.beeHealth = beeHealth
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        self.simpleMovement = simpleMovement


