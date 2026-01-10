from core.Component.Grass import Grass
from core.Component.Hive import Hive
from core.Component.Wall import Wall
from core.Controller.GameController import GameController
from core.GridManager import GridManager
from core.Player import Player
from core.AiPlayer import AiPlayer
from core.view.GameView import GameView
from data.constante import MAX_NECTAR, NECTAR_INITIAL, NFLEURS, WINDOW_TITLE, NCASES, SIZE, TIME_OUT
from gui.Window import Window
from gui.PlayerMenu import get_players_from_menu

class Game:
    def __init__(self):

        self.W = Wall("W")
        self.G = Grass("G")
        self.PLAYERS = get_players_from_menu()

        self.H1 = Hive("h1", self.PLAYERS[0], [], MAX_NECTAR, NECTAR_INITIAL, [])
        self.H2 = Hive("h2", self.PLAYERS[1], [], MAX_NECTAR, NECTAR_INITIAL, [])
        self.H3 = Hive("h3", self.PLAYERS[2], [], MAX_NECTAR, NECTAR_INITIAL, [])
        self.H4 = Hive("h4", self.PLAYERS[3], [], MAX_NECTAR, NECTAR_INITIAL, [])

        self.HIVES = [self.H1, self.H2, self.H3, self.H4]

        self.background = GridManager(NCASES)
        self.background.getBattleZone(self.G)

        self.gm = GridManager(NCASES)
        self.tmp, self.hive_coords = self.gm.addObject(self.W, self.H1, self.H2, self.H3, self.H4)
        self.gm.spawnFlower(NFLEURS)
        self.gm.setSafeZone(self.HIVES)

        self.window = Window(SIZE, WINDOW_TITLE, NCASES)
        self.view = GameView(self.window, self.background, self.gm)
        self.view.render()
        self.moves = []
        self.isup = False
        self.window.track_mouse(self.gm, self.moves, self.isup)
        self.controller = GameController(self.gm, self.HIVES, self.hive_coords, self.view, TIME_OUT)

    def run(self):
        self.controller.run()
        self.window.run()




