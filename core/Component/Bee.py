from core.Player import Player
from core.Component import Hive

class Bee(object):

    def __init__(self,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str ,simpleMovement :bool,motherHive : Hive):
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        self.simpleMovement = simpleMovement
        self.motherHive = motherHive
