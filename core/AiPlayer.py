from logging import raiseExceptions

from core.Player import Player
from core.utilities import randomName
from data.constante import BEES_TYPE
from random import randint


class AiPlayer(Player):

    def __init__(self):
        playerName = "I am an AI player " + randomName()
        primaryColor = "red"
        secondaryColor = "grey"
        isAI = True
        super().__init__(playerName, primaryColor, secondaryColor, isAI)

    def shouldPlay(self , nectar) -> int:
        x = randint(1, 5)
        if x == 1:
            return 3
        y = randint(1, 2)
        return y



    def getBee(self):
        beeIndex = randint(0, 2)
        return BEES_TYPE[beeIndex]


    def aiMoveBee(self, bee , r ,c ):
        from core.Component.Bee import Bee
        if isinstance(bee, Bee):
            x0 = randint(0, 1)
            if x0 == 1:
                x1 = randint(0,1)
                if x1 == 1:
                    r+=1
                else:
                    c+=1
            else:
                x1 = randint(0, 1)
                if x1 == 0:
                    r -= 1
                else:
                    c -= 1
        return r ,c


