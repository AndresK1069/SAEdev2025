import tkinter as tk
from tkinter.ttk import Label
from xxsubtype import bench

from PIL import ImageTk


from core.GridManager import GridManager

from core.Component.Wall import Wall
from core.Component.Grass import Grass
from core.Component.Bees import Bourdon,Eclaireuse,Ouvriere
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from data.constante import NCASES
from gui.Textures import Texture
import copy

class Window:

    def __init__(self,size :int , title :str , ncase : int):
        self.size = size
        self.ncase = ncase
        if self.size % 3 !=0:
            raise Exception("Size must be divisible by 3")
        self.toolTip = None
        self.cellSize = self.size //self.ncase

        self.title = title

        self.window = tk.Tk()


        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size)
        #preloade the assets
        self.sprite_cache = {
            Wall: Texture("assets/wall.png").resize(self.cellSize),
            Grass: Texture("assets/grass.png").resize(self.cellSize),
            Bourdon: Texture("assets/bourdon.png").resize(self.cellSize).getGrayScale(),
            Eclaireuse: Texture("assets/eclaireuse.png").resize(self.cellSize).getGrayScale(),
            Ouvriere: Texture("assets/ouvriere.png").resize(self.cellSize).getGrayScale(),
            Hive: Texture("assets/hive.png").resize(self.cellSize).getGrayScale(),
            Flower: Texture("assets/flower.png").resize(self.cellSize),
            "Cursor": Texture("assets/cursor.png").resize(self.cellSize),
            "Stun": Texture("assets/stun.png").resize(self.cellSize).getGrayScale(),
        }
        self.photo_cache = {}

        self.canvas.pack()

    def drawCell(self):
        """
            Dessine la grille sur le canevas.

            Cette méthode trace les lignes verticales et horizontales pour
            représenter les cellules de la grille de jeu sur le canevas Tkinter.
            La taille de chaque cellule est déterminée par `cellSize`, et le nombre
            total de cases est défini par `NCASES`.

            Retours
            -------
            None
                La méthode agit directement sur le canevas et ne retourne rien.
        """
        for i in range(0, self.cellSize*NCASES, self.cellSize):
            self.canvas.create_line(i, 0, i, self.size, fill="black")
            self.canvas.create_line(0, i, self.size, i, fill="black")

    def getSprite(self, key):
        """
            Récupère une copie d'un sprite depuis le cache.

            Cette méthode retourne une copie indépendante (`deepcopy`) du sprite
            correspondant à la clé fournie. Elle utilise le cache interne
            `sprite_cache` pour éviter de recharger ou recréer les images à chaque fois.

            Paramètres
            ----------
            key : object ou type
                La clé pour identifier le sprite. Cela peut être :
                - un objet dont on veut le sprite,
                - le type de l'objet,
                - ou une clé spécifique (ex. "Stun").

            Retours
            -------
            Sprite | None
                Une copie indépendante du sprite associé à la clé, ou `None` si le sprite
                n'existe pas dans le cache.
        """
        if key in self.sprite_cache:
            return copy.deepcopy(self.sprite_cache[key])

        original_sprite = self.sprite_cache.get(type(key))
        if original_sprite is None:
            return None
        return copy.deepcopy(original_sprite)

    def renderMatrix(self, matrix: GridManager) -> None:
        """
            Affiche graphiquement la matrice de jeu sur le canevas.

            Cette méthode parcourt chaque cellule de la matrice `matrix` et dessine
            les objets qu'elle contient sur le canevas Tkinter.
            - Les cellules peuvent contenir un seul objet ou une liste d'objets.
            - Les abeilles et ruches sont colorisées selon les couleurs de leur propriétaire.
            - Les abeilles étourdies (`stun`) affichent un sprite spécifique.
            - Les objets multiples dans une même cellule sont décalés légèrement pour éviter
              le chevauchement complet.

            Paramètres
            ----------
            matrix : GridManager
                La matrice représentant la grille du jeu contenant les objets à afficher.

            Retours
            -------
            None
                La méthode agit directement sur le canevas et ne retourne rien.
        """
        from core.Component.Bee import Bee

        if not hasattr(self.canvas, "images"):
            self.canvas.images = []

        for r in range(len(matrix.data)):
            for c in range(len(matrix.data[r])):
                cell = matrix.data[r][c]
                if cell is None:
                    continue

                x_pixel = c * self.cellSize
                y_pixel = r * self.cellSize

                objects = cell if isinstance(cell, list) else [cell]
                offset = 0

                for obj in objects:

                    sprite = self.getSprite(obj)
                    if sprite is None:
                        continue

                    if isinstance(obj, (Hive, Bee)) and not (isinstance(obj, Bee) and obj.isStun):
                        color_1 = obj.owner.primaryColor
                        color_2 = obj.owner.secondaryColor
                        sprite.getColorize(color_1, color_2, 0.5)
                        cache_key = (type(obj), color_1, color_2)
                    elif isinstance(obj, Bee) and obj.isStun:
                        cache_key = f"BeeStun_{id(obj)}"
                    else:
                        cache_key = type(obj)


                    self.photo_cache[cache_key] = ImageTk.PhotoImage(sprite.image)
                    img = self.photo_cache[cache_key]
                    self.canvas.images.append(img)
                    self.canvas.create_image(
                        x_pixel + offset,
                        y_pixel + offset,
                        image=img,
                        anchor="nw"
                    )

                    if isinstance(obj, Bee) and obj.isStun:
                        stun_sprite = self.getSprite("Stun")
                        stun_cache_key = f"Stun_{id(obj)}"
                        self.photo_cache[stun_cache_key] = ImageTk.PhotoImage(stun_sprite.image)
                        stun_img = self.photo_cache[stun_cache_key]
                        self.canvas.images.append(stun_img)
                        self.canvas.create_image(
                            x_pixel + offset,
                            y_pixel + offset,
                            image=stun_img,
                            anchor="nw"
                        )

                    offset += 5

    def track_mouse(self, matrix: GridManager, lastLoc: list, isUp: bool):
        """
          Suit le curseur de la souris et affiche un tooltip pour la cellule survolée.

          Cette méthode vérifie périodiquement la position de la souris sur le canevas,
          calcule la cellule correspondante dans la matrice `matrix` et affiche un tooltip
          contenant les informations de la cellule si elle est survolée.
          - Les cellules vides ou les murs (`Wall`) ne déclenchent pas de tooltip.
          - Le tooltip disparaît lorsque la souris quitte la cellule ou survole une cellule
            vide ou un mur.

          La méthode s'auto-appelle toutes les 50 ms via `self.window.after` pour un suivi
          continu de la souris.

          Paramètres
          ----------
          matrix : GridManager
              La matrice représentant la grille du jeu.
          lastLoc : list
              Liste contenant les coordonnées de la dernière cellule survolée.
              Permet de gérer l'affichage du tooltip pour éviter les répétitions.
          isUp : bool
              Indique si le tooltip est actuellement affiché ou non.

          Retours
          -------
          None
              La méthode agit directement sur l'interface graphique et le tooltip,
              elle ne retourne rien.
        """
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        if x < self.size and y < self.size:
            col = x // self.cellSize  # column index
            row = y // self.cellSize  # row index
            if matrix.data[row][col] is not None:
                if not isinstance(matrix.data[row][col], Wall):
                    if len(lastLoc) == 0:
                        lastLoc[:] = [row, col]
                        isUp = False
                    if len(lastLoc) == 2 and lastLoc[0] == row and lastLoc[1] == col:
                        if not hasattr(self, "toolTip") or self.toolTip is None:
                            isUp = True
                            self.toolTip = Label(self.window,text=self.getInfo(matrix.data[row][col]),anchor="center",background="lightblue")
                            self.toolTip.pack()
                    if len(lastLoc) == 2 and (lastLoc[0] != row or lastLoc[1] != col):
                        if hasattr(self, "toolTip") and self.toolTip is not None:
                            lastLoc.clear()
                            isUp = False
                            self.toolTip.destroy()
                            self.toolTip = None
            if matrix.data[row][col] is None or isinstance(matrix.data[row][col], Wall):
                if hasattr(self, "toolTip") and self.toolTip is not None:
                    lastLoc.clear()
                    isUp = False
                    self.toolTip.destroy()
                    self.toolTip = None

        self.window.after(50, self.track_mouse, matrix, lastLoc, isUp)

    def canvaClear(self):
        """
            Efface entièrement le canevas graphique.

            La méthode supprime tous les objets dessinés sur le canevas et
            vide la liste interne des images associées.

            Retours
            -------
            None
                La méthode ne retourne rien ; elle agit directement sur le canevas.
        """
        self.canvas.delete("all")
        self.canvas.images.clear()

    def waitForClick(self):
        """
            Attend qu'un clic de souris se produise sur le canevas et retourne la position.

            La méthode bloque l'exécution jusqu'à ce que l'utilisateur clique
            sur le canevas. Elle calcule la cellule cliquée en fonction de la
            taille des cellules (`cellSize`) et retourne ses coordonnées
            (ligne, colonne).

            Retours
            -------
            tuple[int, int]
                Coordonnées (row, col) de la cellule cliquée sur le canevas.
        """
        self._click_var = tk.IntVar()
        self._click_pos = None

        def on_click(event):
            col = event.x // self.cellSize
            row = event.y // self.cellSize
            self._click_pos = (row, col)
            self._click_var.set(1)

        self.canvas.bind("<Button-1>", on_click)
        self.window.wait_variable(self._click_var)
        self.canvas.unbind("<Button-1>")

        return self._click_pos

    def getInfo(self,cell):
        """
            Retourne une chaîne descriptive contenant les informations sur une cellule.

            Selon le type de cellule, la méthode fournit différentes informations :
            - **Flower** : indique simplement "Fleur".
            - **Hive** : affiche le nom du propriétaire de la ruche.
            - **Bee** : si l'abeille est étourdie (stun), affiche le propriétaire et le nombre de tours restants.
            - **Eclaireuse / Ouvrière / Bourdon** : affiche un résumé détaillé de l'abeille, incluant :
                - Type d'abeille
                - Nom de l'abeille
                - Propriétaire
                - Vie actuelle et maximale
                - Force
                - Nectar actuel et maximal

            Paramètres
            ----------
            cell : object
                La cellule à inspecter. Peut être une `Flower`, `Hive` ou une abeille (`Bee`, `Eclaireuse`, `Ouvriere`, `Bourdon`).

            Retours
            -------
            str
                Une chaîne décrivant les informations pertinentes de la cellule.
        """
        from core.Component.Bee import Bee
        if isinstance(cell, Flower):
            f =f"Fleur"
            return f
        if isinstance(cell , Hive):
            f=f"Propriétaire : {cell.owner.playerName}"
            return f

        if isinstance(cell, Bee):
            if cell.isStun:
                f = f"Propriétaire : {cell.owner.playerName}\nTours Restants : {cell.stunCounter}"
                return f

        if isinstance(cell , Eclaireuse):
            f = f"Abeillie : Eclaireuse\nNom de L'abeille : {cell.name}\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f
        if isinstance(cell, Ouvriere):
            f = f"Abeillie : Ouvriere\nNom de L'abeille : {cell.name}\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f
        if isinstance(cell, Bourdon):
            f = f"Abeillie : Bourdon\n Nom de L'abeille : {cell.name}\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f

    def run(self):
        """
            Lance la boucle principale de l'interface graphique.

            Cette méthode démarre la boucle `mainloop` de Tkinter pour
            maintenir la fenêtre ouverte et permettre l'interaction
            avec l'utilisateur.

            Retours
            -------
            None
                La méthode ne retourne rien ; elle exécute la boucle graphique.
        """
        self.window.mainloop()
