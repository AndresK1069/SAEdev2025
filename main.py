from core.Component.Grass import Grass
from core.Component.Hive import Hive
from core.Component.Wall import Wall
from core.Controller.GameController import GameController
from core.GridManager import GridManager
from core.Player import Player
from core.utilities import randomName
from core.view.GameView import GameView
from data.constante import MAX_NECTAR, NECTAR_INITIAL, NFLEURS, WINDOW_TITLE, NCASES, SIZE, TIME_OUT
from gui.Window import Window


W = Wall("W")
G = Wall("G")

empty_b = []

inputP1 = "j1"
inputP2 = "j2"
inputP3 = "j3"
inputP4 = "j4"

p1 = Player(inputP1,"red","yellow")
p2 = Player(inputP2,"gold","green")
p3 = Player(inputP3,"coral","cyan")
p4 = Player(inputP4,"pink","purple")

PLAYERS = [p1,p2,p3,p4]

H1 = Hive("h1",p1 ,[],MAX_NECTAR,NECTAR_INITIAL ,[])
H2 = Hive("h2",p2,[],MAX_NECTAR,NECTAR_INITIAL,[])
H3 = Hive("h3",p3,[],MAX_NECTAR,NECTAR_INITIAL,[])
H4 = Hive("h4",p4,[],MAX_NECTAR,NECTAR_INITIAL,[])

HIVES = [H1,H2,H3,H4]

G= Grass("G")
background = GridManager(NCASES)
background.getBattleZone(G)

gm = GridManager(NCASES)
tmp, hive_coords = gm.addObject(W, H1, H2, H3, H4)
gm.spawnFlower(NFLEURS)


window = Window(SIZE, WINDOW_TITLE, NCASES)
view = GameView(window, background, gm)
view.render()
moves=[]
isup=False
window.track_mouse(gm,moves,isup)


controller = GameController(gm, HIVES, hive_coords, view, TIME_OUT)
controller.run()
window.run()