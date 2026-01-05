import tkinter as tk
from tkinter import simpledialog

from core.Component.Hive import Hive
from core.GridManager import GridManager
from gui.Window import Window


class GameView:

    def __init__(self, window:Window,background: GridManager ,grid: GridManager):
        self.window = window
        self.background = background
        self.grid = grid

    def render(self):
        self.grid.render()
        self.window.renderMatrix(self.background)
        self.window.drawCell()
        self.window.renderMatrix(self.grid)

    def clearCanva(self)->None:
        self.window.canvaClear()


    def show_player(self, hive:Hive):
        print(f"\nPlayer : {hive.owner.playerName}")
        print(f"Nectar actuel : {hive.currentNectar}")

    def show_menu(self):
        print("1. Pondre")
        print("2. Bouger une abeille")
        print("3. Passer le tour")

    def ask_choice(self, hive:Hive):
        choice = simpledialog.askinteger(
            "Action",
            f"Joueur : {hive.owner.playerName}\nNectar Actuelle : {hive.getNectar()}\n \nchoisissez une action :\n1: Pondre\n2: Bouger\n3: Passer le tour",
            minvalue=1,
            maxvalue=3
        )
        return choice


    def ask_choice2(self, hive):
        popup = tk.Toplevel()
        popup.title("Action")
        popup.geometry("300x200")
        popup.resizable(False, False)

        selected_choice = {"value": None}

        tk.Label(
            popup,
            text=f"Joueur : {hive.owner.playerName}\nNectar Actuelle : {hive.getNectar()}\n\nChoisissez une action :",
            justify="left"
        ).pack(pady=10)

        def choose(val):
            selected_choice["value"] = val
            popup.destroy()

        tk.Button(popup, text="1: Pondre", width=20, command=lambda: choose(1)).pack(pady=5)
        tk.Button(popup, text="2: Bouger", width=20, command=lambda: choose(2)).pack(pady=5)
        tk.Button(popup, text="3: Passer le tour", width=20, command=lambda: choose(3)).pack(pady=5)

        popup.grab_set()
        popup.wait_window()

        return selected_choice["value"]