from core.Component.Bee import Bee

class Eclaireuse(Bee):
    def __init__(self):
        beeHealth = 3
        maxNectar = 5
        beeAgility = 0
        beeStrength = 1
        displayObject = "E"
        simpleMovement = False

        super().__init__(beeHealth, maxNectar, beeAgility, beeStrength, displayObject, simpleMovement)
