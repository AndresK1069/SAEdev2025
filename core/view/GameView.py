from core.Component.Hive import Hive
from core.GridManager import GridManager
from graphic.Window import Window


class GameView:

    def __init__(self, window:Window,background: GridManager ,grid: GridManager):
        self.window = window
        self.background = background
        self.grid = grid

    def render(self):
        self.window.renderMatrix(self.background)
        self.window.drawCell()
        self.window.renderMatrix(self.grid)

    def clearCanva(self):
        self.window.canvaClear()


    def show_player(self, hive:Hive):
        print(f"\nPlayer : {hive.owner.playerName}")
        print(f"Nectar actuel : {hive.currentNectar}")

    def show_menu(self):
        print("1. Pondre")
        print("2. Bouger une abeille")
        print("3. Passer le tour")

    def ask_choice(self):
        return input("Entrez un choix : ")
