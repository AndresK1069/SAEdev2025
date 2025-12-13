from core.Component.Bee import Bee

class Eclaireuse(Bee):
    def __init__(self):
        beeHealth = 3
        maxNectar = 5
        beeAgility = 3
        beeStrength = 1
        displayObject = "E"
        simpleMovement = False
        nectarCost = 0
        currentNectar = 0
        super().__init__(beeHealth, maxNectar, beeAgility, beeStrength, displayObject, simpleMovement,nectarCost, currentNectar)
