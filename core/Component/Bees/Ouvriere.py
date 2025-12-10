from core.Component.Bee import Bee

class Ouvriere(Bee):
    def __init__(self):
        beeHealth = 5
        maxNectar = 12
        beeAgility = 1
        beeStrength = 1
        displayObject = "O"
        simpleMovement = True
        super().__init__(beeHealth, maxNectar, beeAgility, beeStrength, displayObject, simpleMovement)