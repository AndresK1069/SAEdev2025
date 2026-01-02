import tkinter as tk
from tkinter.ttk import Label

from PIL import ImageTk


from core.GridManager import GridManager

from core.Component.Wall import Wall
from core.Component.Grass import Grass
from core.Component.Bees import Bourdon,Eclaireuse,Ouvriere
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from data.constante import NCASES
from gui.Textures import Texture


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
        self.window.title(self.title)

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
        }

        self.canvas.pack()

    def drawCell(self):
        for i in range(0, self.cellSize*NCASES, self.cellSize):
            self.canvas.create_line(i, 0, i, self.size, fill="black")
            self.canvas.create_line(0, i, self.size, i, fill="black")

    def getSprite(self, cell):
        return self.sprite_cache.get(type(cell))

    def renderMatrix(self, matrix: GridManager) -> None:
        from core.Component.Bee import Bee
        #FIXME handle stun bees
        if not hasattr(self.canvas, "images"):
            self.canvas.images = []

        for r in range(len(matrix.data)):
            for c in range(len(matrix.data[r])):
                cell = matrix.data[r][c]
                if cell is None:
                    continue

                x_pixel = c * self.cellSize
                y_pixel = r * self.cellSize

                # Multiple objects in one cell
                if isinstance(cell, list):
                    offset = 0
                    for obj in cell:
                        sprite = self.getSprite(obj)
                        if isinstance(obj, Hive) or isinstance(obj, Bee):
                            color_1 = obj.owner.primaryColor
                            color_2 =obj.owner.secondaryColor
                            sprite.getColorize(color_1, color_2,0.5)

                        if sprite is None:
                            continue
                        img = ImageTk.PhotoImage(sprite.image)
                        self.canvas.images.append(img)
                        self.canvas.create_image(
                            x_pixel + offset,
                            y_pixel + offset,
                            image=img,
                            anchor="nw"
                        )
                        offset += 5
                    continue

                # Single object
                sprite = self.getSprite(cell)
                if isinstance(cell, Hive) or isinstance(cell, Bee):
                    color_1 = cell.owner.primaryColor
                    color_2 = cell.owner.secondaryColor
                    sprite.getColorize(color_1, color_2, 0.5)
                if sprite is None:
                    continue
                img = ImageTk.PhotoImage(sprite.image)
                self.canvas.images.append(img)
                self.canvas.create_image(
                    x_pixel,
                    y_pixel,
                    image=img,
                    anchor="nw"
                )

    def track_mouse(self, matrix: GridManager, lastLoc: list, isUp: bool):
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
        self.canvas.delete("all")

    def waitForClick(self):
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
        if isinstance(cell, Flower):
            f =f"Nectar actuelle : {cell.flowerNectar}"
            return f
        if isinstance(cell , Hive):
            f=f"Propriétaire : {cell.owner.playerName}"
            return f
        if isinstance(cell , Eclaireuse):
            f = f"Abeillie : Eclaireuse\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}\nTours Restants(si Escarmouche) : {cell.stunCounter}"
            return f
        if isinstance(cell, Ouvriere):
            f = f"Abeillie : Ouvriere\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}\nTours Restants(si Escarmouche) : {cell.stunCounter}"
            return f
        if isinstance(cell, Bourdon):
            f = f"Abeillie : Bourdon\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}\nTours Restants(si Escarmouche) : {cell.stunCounter}"
            return f


    def run(self):
        self.window.mainloop()
