from GridManager import GridManager
from data.constante import NCASES

from core.Component.Wall import Wall
from core.Component.Flower import Flower
from core.Component.Hive import Hive
from core.Player import Player
from data.constante import NFLEURS
from data.constante import NECTAR_INITIAL
from data.constante import MAX_NECTAR
from data.constante import TIME_OUT


W= Wall("W")
G =Wall("G")

empty_b = []

p1 = Player(NECTAR_INITIAL,MAX_NECTAR)
p2 = Player(NECTAR_INITIAL,MAX_NECTAR)
p3 = Player(NECTAR_INITIAL,MAX_NECTAR)
p4 = Player(NECTAR_INITIAL,MAX_NECTAR)

PLAYERS = [p1,p2,p3,p4]

H1 = Hive("h1",p1 ,[])
H2 = Hive("h2",p2,[])
H3 = Hive("h3",p3,[])
H4 = Hive("h4",p3,[])

HIVES = [H1,H2,H3,H4]

F = Flower("f")

gm = GridManager(NCASES)
tmp, hive_coords = gm.addObject(W, H1, H2, H3, H4)
print(hive_coords)
gm.spawnFlower(F,NFLEURS)
gm.render()

while TIME_OUT > 0:

    for i in range(len(HIVES)):


        # Spawing Prototype (Working)

        row , col = hive_coords[i]
        gm.data[row][col] = gm.cellToList(row, col)
        bee_ = HIVES[i].spawnBee("Bourdon")
        gm.data[row][col].append(bee_)
        print(HIVES[i].beeList)
        print(gm.data[row][col])



    #TODO change this when logic working
    break

