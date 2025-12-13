from GridManager import GridManager

from core.Component.Wall import Wall
from core.Component.Flower import Flower
from core.Component.Hive import Hive
from core.Player import Player
from core.Component.Bees.BeeTypes import *

from data.constante import NFLEURS
from data.constante import NECTAR_INITIAL
from data.constante import MAX_NECTAR
from data.constante import TIME_OUT
from data.constante import NCASES


W= Wall("W")
G =Wall("G")

empty_b = []

inputP1 = input("Nom du Joueur 1:")
inputP2 = input("Nom du Joueur 2:")
inputP3 = input("Nom du Joueur 3:")
inputP4 = input("Nom du Joueur 4:")

p1 = Player(NECTAR_INITIAL,inputP1)
p2 = Player(NECTAR_INITIAL,inputP2)
p3 = Player(NECTAR_INITIAL,inputP3)
p4 = Player(NECTAR_INITIAL,inputP4)

PLAYERS = [p1,p2,p3,p4]

H1 = Hive("h1",p1 ,[],MAX_NECTAR,0)
H2 = Hive("h2",p2,[],MAX_NECTAR,0)
H3 = Hive("h3",p3,[],MAX_NECTAR,0)
H4 = Hive("h4",p4,[],MAX_NECTAR,0)

HIVES = [H1,H2,H3,H4]

F = Flower("f", NECTAR_INITIAL)

gm = GridManager(NCASES)
tmp, hive_coords = gm.addObject(W, H1, H2, H3, H4)
#print(hive_coords)
gm.spawnFlower(F,NFLEURS)
gm.render()

while TIME_OUT > 0:
    for i in range(len(HIVES)):
        print(f"Player :{HIVES[i].owner.playerName}")
        print(f"nectar actuelle :{HIVES[i].owner.playerNectarInitial}")
        print("faite un choix")
        print(" 1. Pondre")
        print(" 2. Bouger un abielle")
        choice = input("entrez un choix : ")

        if choice == "1":

            # Spawing Prototype (Working)

            print(f"nectar actuelle :{HIVES[i].owner.playerNectarInitial}")

            beePlayerInput = input("Pondre une abeille : ")

            #TODO Move to its own method

            beePlayerInput.lower()
            bee_class = BEE_TYPES[beePlayerInput]
            DummyObjectbeeData = bee_class()

            #check if player have enough nectar and if yes  spawn bee
            #TODO change when not enough nectar
            if HIVES[i].owner.playerNectarInitial >= DummyObjectbeeData.nectarCost:

                HIVES[i].owner.playerNectarInitial -= DummyObjectbeeData.nectarCost
                print(HIVES[i].owner.playerNectarInitial)

                row , col = hive_coords[i]
                gm.data[row][col] = gm.cellToList(row, col)
                bee_ = HIVES[i].spawnBee(beePlayerInput)
                gm.data[row][col].append(bee_)
                print(HIVES[i].beeList)
                print(gm.data[row][col])

                del DummyObjectbeeData
                gm.render()

        #MOVEMENTE
        if len(HIVES[i].beeList) != 0:
            #print("can move")
            for bee in HIVES[i].beeList:
                newRow = int(input("Nouvelle ligne :"))
                newCol = int(input("Nouvelle Column :"))
                gm.moveObject(bee ,newRow,newCol)
                gm.cleanGrid()
                gm.render()
        else:
            print("can't move")

    winner_array=[]
    for i in range(HIVES):
        if HIVES[i].currentNectar == HIVES[i].maxNectar:
            winner_array.append(HIVES[i].owner.playerName)
        for bee in HIVES[i].beeList:
            # Scanner au tour de bee pour check si il y'a du nectar ou escarmouches
            pass

    # fin de Gagnant
    if len(winner_array) != 0:
        if len(winner_array) == 1:
            print(f"{winner_array[0]} a gagnez !!!")
        else:
            for name in winner_array:
                print(name)
            print("Sont arriver ex aequo")
        break

    #TODO at the end of every check for fights and flower




    TIME_OUT -= 1

