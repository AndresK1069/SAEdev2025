import tkinter as tk
from tkinter import simpledialog
from core.Component.Hive import Hive
from core.GridManager import GridManager
from gui.Window import Window
from data.constante import BEES_TYPE


class GameView:

    def __init__(self, window:Window,background: GridManager ,grid: GridManager):
        self.window = window
        self.background = background
        self.grid = grid

    def render(self):
        """
           Met à jour l'affichage complet du jeu.

           Cette méthode effectue les opérations suivantes dans l'ordre :
           1. Rend la grille de jeu avec les objets actuels (`self.grid.render()`).
           2. Affiche l'arrière-plan sur le canevas avec `renderMatrix`.
           3. Dessine la grille (lignes de séparation des cases) avec `drawCell`.
           4. Affiche à nouveau la grille de jeu par-dessus l'arrière-plan pour s'assurer que tous les objets sont visibles.

           Paramètres
           ----------
           Aucun

           Retours
           -------
           None
               La méthode agit directement sur l'affichage, sans retourner de valeur.
        """
        self.grid.render()
        self.window.renderMatrix(self.background)
        self.window.drawCell()
        self.window.renderMatrix(self.grid)

    def clearCanva(self)->None:
        """
            Efface complètement le canevas de la fenêtre de jeu.

            Cette méthode supprime tous les éléments graphiques du canevas et vide la liste interne
            des images afin de préparer le canevas pour un nouveau rendu.

            Paramètres
            ----------
            Aucun

            Retours
            -------
            None
                La méthode agit directement sur le canevas, sans retourner de valeur.
        """
        self.window.canvaClear()


    def show_player(self, hive:Hive):
        """
            Affiche les informations principales d'un joueur et de sa ruche.

            Cette méthode affiche dans la console :
            - Le nom du joueur propriétaire de la ruche.
            - Le nectar actuel disponible dans la ruche.

            Paramètres
            ----------
            hive : Hive
                La ruche dont on souhaite afficher les informations.

            Retours
            -------
            None
                La méthode n'affiche les informations que dans la console et ne retourne rien.
        """
        print(f"\nPlayer : {hive.owner.playerName}")
        print(f"Nectar actuel : {hive.currentNectar}")

    def show_menu(self):
        """
           Affiche le menu des actions disponibles pour le joueur.

           Cette méthode affiche dans la console les options suivantes :
           1. Pondre une nouvelle abeille.
           2. Bouger une abeille existante.
           3. Passer le tour sans effectuer d'action.

           Paramètres
           ----------
           Aucun

           Retours
           -------
           None
               La méthode n'affiche le menu que dans la console et ne retourne rien.
        """
        print("1. Pondre")
        print("2. Bouger une abeille")
        print("3. Passer le tour")

    def ask_choice(self, hive:Hive):
        """
            Demande au joueur de choisir une action pour son tour via une boîte de dialogue.

            La boîte de dialogue affiche :
            - Le nom du joueur propriétaire de la ruche.
            - Le nectar actuel disponible dans la ruche.
            - Les trois actions possibles :
                1. Pondre une nouvelle abeille.
                2. Bouger une abeille existante.
                3. Passer le tour.

            Paramètres
            ----------
            hive : Hive
                La ruche du joueur pour laquelle l'action doit être choisie.

            Retours
            -------
            int
                L'entier correspondant au choix du joueur (1, 2 ou 3).
        """
        choice = simpledialog.askinteger(
            "Action",
            f"Joueur : {hive.owner.playerName}\nNectar Actuelle : {hive.getNectar()}\n \nchoisissez une action :\n1: Pondre\n2: Bouger\n3: Passer le tour",
            minvalue=1,
            maxvalue=3
        )
        return choice


    def ask_choice2(self, hive):
        """
            Affiche une fenêtre pop-up pour que le joueur choisisse une action pour son tour.

            La fenêtre affiche :
            - Le nom du joueur propriétaire de la ruche.
            - Le nectar actuel de la ruche.
            - Trois boutons correspondant aux actions possibles :
                1. Pondre une nouvelle abeille.
                2. Bouger une abeille existante.
                3. Passer le tour.

            Paramètres
            ----------
            hive : Hive
                La ruche du joueur pour laquelle l'action doit être choisie.

            Retours
            -------
            int
                L'entier correspondant au choix du joueur (1, 2 ou 3).
        """
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

    def choose_bee(self,hive):
        bee_options = BEES_TYPE

        popup = tk.Toplevel()
        popup.title(f"{hive.owner.playerName} Spawn Bee")
        popup.geometry("250x200")
        popup.resizable(False, False)

        tk.Label(popup, text="Nom de l'abeille :", font=("Arial", 12)).pack(pady=5)


        frame = tk.Frame(popup)
        frame.pack(pady=5, padx=5, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, height=6)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.pack(side="left", fill="both", expand=True)

        for bee in bee_options:
            listbox.insert(tk.END, bee)

        selected_bee = {"value": None}

        def confirm_selection():
            selection = listbox.curselection()
            if selection:
                selected_bee["value"] = listbox.get(selection[0])
                popup.destroy()

        tk.Button(popup, text="OK", command=confirm_selection).pack(pady=5)

        popup.grab_set()
        popup.wait_window()

        return selected_bee["value"]