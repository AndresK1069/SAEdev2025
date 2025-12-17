from GridManager import GridManager

from core.Component.Wall import Wall
from core.Component.Flower import Flower
from core.Component.Hive import Hive
from core.Component.Bees.BeeTypes import *
from core.Player import Player
from core.utilities import evenSplit

from data.constante import COUT_PONTE
from data.constante import NFLEURS
from data.constante import NECTAR_INITIAL
from data.constante import MAX_NECTAR
from data.constante import TIME_OUT
from data.constante import NCASES


W= Wall("W")
G =Wall("G")

empty_b = []

inputP1 = "j1"
inputP2 = "j2"
inputP3 = "j3"
inputP4 = "j4"

p1 = Player(inputP1)
p2 = Player(inputP2)
p3 = Player(inputP3)
p4 = Player(inputP4)

PLAYERS = [p1,p2,p3,p4]

H1 = Hive("h1",p1 ,[],MAX_NECTAR,NECTAR_INITIAL)
H2 = Hive("h2",p2,[],MAX_NECTAR,NECTAR_INITIAL)
H3 = Hive("h3",p3,[],MAX_NECTAR,NECTAR_INITIAL)
H4 = Hive("h4",p4,[],MAX_NECTAR,NECTAR_INITIAL)

HIVES = [H1,H2,H3,H4]

F = Flower("f", evenSplit(NFLEURS,MAX_NECTAR))

gm = GridManager(NCASES)
tmp, hive_coords = gm.addObject(W, H1, H2, H3, H4)
#print(hive_coords)
gm.spawnFlower(F,NFLEURS)





while TIME_OUT > 0:
    for i in range(len(HIVES)):
        gm.render()
        print(f"Player :{HIVES[i].owner.playerName}")
        print(f"nectar actuelle :{HIVES[i].currentNectar}")
        print("faite un choix")
        print(" 1. Pondre")
        print(" 2. Bouger un abielle")
        print(" 3. passer le tour")
        choice = input("entrez un choix : ")

        if choice == "1" and HIVES[i].currentNectar >= COUT_PONTE:

            # Spawing Prototype (Working)

            print(f"nectar actuelle :{HIVES[i].currentNectar}")

            beePlayerInput = input("Pondre une abeille : ")

            #TODO Move to its own method

            beePlayerInput.lower()
            bee_class = BEE_TYPES[beePlayerInput]
            DummyObjectbeeData = bee_class()

            row, col = hive_coords[i]
            gm.data[row][col] = gm.cellToList(row, col)


            if HIVES[i].currentNectar >= COUT_PONTE and len(gm.data[row][col])==1:
                HIVES[i].currentNectar -= COUT_PONTE
                print(HIVES[i].currentNectar)
                bee_ = HIVES[i].spawnBee(beePlayerInput)
                gm.data[row][col].append(bee_)
                print(HIVES[i].beeList)
                print(gm.data[row][col])

                del DummyObjectbeeData
                gm.render()


        #MOVEMENTE
        if len(HIVES[i].beeList) != 0:
            for bee in HIVES[i].beeList:
                if not bee.isStun:
                    print(f"voulez vous bouger l'abeille {bee}")
                    print(f"nectar actuelle :{bee.currentNectar}")
                    skip = int(input("entrez un skip : "))
                    if skip == 1:
                        newRow = int(input("Nouvelle ligne :"))
                        newCol = int(input("Nouvelle Column :"))
                        gm.moveObject(bee ,newRow,newCol)
                        gm.cleanGrid()
                        gm.render()
                    else:
                        continue
                else:
                    print(f"il vous reste {bee.stunCounter} avant de pouvoir bouger")
                    bee.stunCounter -= 1

        else:
            print("can't move")

        if choice == "3":
            continue


    winner_array=[]
    for i in range(len(HIVES)):
        if HIVES[i].currentNectar == HIVES[i].maxNectar:
            winner_array.append(HIVES[i].owner.playerName)


    arr_f = gm.recupFleur()
    gm.getBeePos()
    gm.flowerButinage(arr_f)
    gm.emptyBeeNectar(hive_coords)
    gm.checkEscarmouche()
    gm.checkBeeHealth()

    #fin de Gagnant
    #TODO RE-work winning condition
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

