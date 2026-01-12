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

    def shouldPlay(self,nectar) -> int:
        """
            Détermine de manière aléatoire si une action doit être effectuée.

            La méthode génère un nombre aléatoire pour décider du comportement
            à adopter.

            Logique :
            - Avec une chance sur 5 (`randint(1, 5) == 1`), retourne 3.
            - Sinon, retourne soit 1 soit 2 (`randint(1, 2)`).

            Retours
            -------
            int
                Valeur aléatoire déterminant l'action : 1, 2 ou 3.
        """
        x = randint(1, 5)
        if x == 1:
            return 3
        y = randint(1, 2)
        return y

    def getBee(self):
        """
            Sélectionne aléatoirement un type d'abeille depuis la liste `BEES_TYPE`.

            La méthode choisit un indice aléatoire valide en fonction de la
            longueur actuelle de la liste `BEES_TYPE` et retourne le type
            d'abeille correspondant.

            Retours
            -------
            any
                Un type d'abeille sélectionné aléatoirement depuis `BEES_TYPE`.
        """
        beeIndex = randint(0,   (len(BEES_TYPE) - 1))
        return BEES_TYPE[beeIndex]

    def aiMoveBee(self, bee , r ,c ):
        """
            Génère un déplacement aléatoire pour une abeille contrôlée par l'IA.

            La méthode modifie les coordonnées (r, c) de l'abeille de manière
            aléatoire selon une logique simple :
            - Choix aléatoire d'une direction principale (augmenter ou diminuer).
            - Choix aléatoire de l'axe à modifier (ligne ou colonne).

            Paramètres
            ----------
            bee : Bee
                L'objet abeille à déplacer. Se déplace uniquement si `bee` est de type `Bee`.
            r : int
                Coordonnée de ligne actuelle de l'abeille.
            c : int
                Coordonnée de colonne actuelle de l'abeille.

            Retours
            -------
            tuple[int, int]
                Nouvelles coordonnées (ligne, colonne) après déplacement aléatoire.
            """
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


