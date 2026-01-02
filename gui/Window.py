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
            "Cursor": Texture("assets/cursor.png").resize(self.cellSize),
            "Stun": Texture("assets/stun.png").resize(self.cellSize).getGrayScale(),
        }
        self.photo_cache = {}

        self.canvas.pack()

    def drawCell(self):
        for i in range(0, self.cellSize*NCASES, self.cellSize):
            self.canvas.create_line(i, 0, i, self.size, fill="black")
            self.canvas.create_line(0, i, self.size, i, fill="black")

    def getSprite(self, key):
        if key in self.sprite_cache:
            return copy.deepcopy(self.sprite_cache[key])

        original_sprite = self.sprite_cache.get(type(key))
        if original_sprite is None:
            return None
        return copy.deepcopy(original_sprite)

    def renderMatrix(self, matrix: GridManager) -> None:
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
        self.canvas.images.clear()

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
        from core.Component.Bee import Bee
        if isinstance(cell, Flower):
            f =f"Nectar actuelle : {cell.flowerNectar}"
            return f
        if isinstance(cell , Hive):
            f=f"Propriétaire : {cell.owner.playerName}"
            return f

        if isinstance(cell, Bee):
            if cell.isStun:
                f = f"Propriétaire : {cell.owner.playerName}\nTours Restants : {cell.stunCounter}"
                return f

        if isinstance(cell , Eclaireuse):
            f = f"Abeillie : Eclaireuse\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f
        if isinstance(cell, Ouvriere):
            f = f"Abeillie : Ouvriere\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f
        if isinstance(cell, Bourdon):
            f = f"Abeillie : Bourdon\nPropriétaire : {cell.owner.playerName}\nVie : {cell.currenthealth}/{cell.beeHealth}\nForce : {cell.beeStrength}\nNectar actuelle : {cell.currentNectar}/{cell.maxNectar}"
            return f


    def run(self):
        self.window.mainloop()
