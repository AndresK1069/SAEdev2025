from core.Player import Player


class Bee(object):

    def __init__(self ,owner : Player ,maxNectar : int , beeAgility : int , beeStrength : int , displayObject: str):
        self.owner = owner
        self.maxNectar = maxNectar
        self.beeAgility = beeAgility
        self.beeStrength = beeStrength
        self.displayObject = displayObject
        pass