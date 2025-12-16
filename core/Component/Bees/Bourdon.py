from core.Component.Bee import Bee

class Bourdon(Bee):
    def __init__(self):
        beeHealth = 5
        maxNectar = 3
        beeAgility = 2
        beeStrength = 5
        displayObject = "B"
        simpleMovement = True
        currentNectar = 0
        stunCounter =0
        moveList = []
        isStun = False
        currenthealth = beeHealth
        super().__init__(beeHealth, maxNectar, beeAgility, beeStrength, displayObject, simpleMovement, currentNectar,stunCounter, moveList, isStun, currenthealth)
