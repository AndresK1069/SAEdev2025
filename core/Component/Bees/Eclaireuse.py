from core.Component.Bee import Bee

class Eclaireuse(Bee):
    def __init__(self):
        beeHealth = 3
        maxNectar = 5
        beeAgility = 99
        beeStrength = 1
        displayObject = "E"
        simpleMovement = False
        currentNectar = 0
        stunCounter = 0
        moveList = []
        isStun = False
        currenthealth = beeHealth
        owner = None
        super().__init__(beeHealth, maxNectar, beeAgility, beeStrength, displayObject, simpleMovement, currentNectar,stunCounter, moveList, isStun, currenthealth, owner)
