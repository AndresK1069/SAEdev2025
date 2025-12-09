from GridManager import GridManager
from data.constante import NCASES

from core.Component.Wall import Wall
from core.Component.Flower import Flower
from core.Component.Hive import Hive
from core.Player import Player
from data.constante import NFLEURS


W= Wall("W")
G =Wall("G")

p1 = Player()
p2 = Player()
p3 = Player()
p4 = Player()

F = Flower("f")
H1 = Hive("h1",p1)
H2 = Hive("h2",p2)
H3 = Hive("h3",p3)
H4 = Hive("h4",p3)



gm = GridManager(NCASES)
gm.addObject(W, H1, H2, H3, H4)
gm.spawnFlower(F,NFLEURS)
gm.render()

