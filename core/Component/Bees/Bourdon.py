from core.Component.Bee import Bee

class Bourdon(Bee):
    def __init__(self):
        beeHealth = 5
        maxNectar = 3
        beeAgility = 2
        beeStrength = 5
        displayObject = "B"
        simpleMovement = True

        super().__init__(beeHealth,maxNectar, beeAgility, beeStrength, displayObject, simpleMovement)
