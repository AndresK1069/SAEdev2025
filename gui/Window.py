import tkinter as tk
from core.GridManager import GridManager

from core.Component.Wall import Wall
from core.Component.Grass import Grass
from core.Component.Bees import Bourdon,Eclaireuse,Ouvriere
from core.Component.Hive import Hive
from core.Component.Flower import Flower
from data.constante import NCASES


class Window:

    def __init__(self,size :int , title :str , ncase : int):
        self.size = size
        self.ncase = ncase
        if self.size % 3 !=0:
            raise Exception("Size must be divisible by 3")

        self.cellSize = self.size //self.ncase

        self.title = title

        self.window = tk.Tk()
        self.window.title(self.title)

        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size)
        self.canvas.pack()

    def drawCell(self):
        for i in range(0, self.cellSize*NCASES, self.cellSize):
            self.canvas.create_line(i, 0, i, self.size, fill="black")
            self.canvas.create_line(0, i, self.size, i, fill="black")


    def getSprite(self , cell):

        if cell is None:
            pass

        dicSprite = {
            Wall:"grey",
            Grass:"green",
            Bourdon:"gold",
            Eclaireuse:"deep sky blue",
            Ouvriere:"red",
            Hive:"yellow",
            Flower:"pink"
        }
        return dicSprite.get(type(cell))

    def renderMatrix(self, matrix :GridManager) -> None:
        for r in range(len(matrix.data)):
            for c in range(len(matrix.data)):

                if matrix.data[r][c] is None:
                    pass

                if isinstance(matrix.data[r][c], list):
                    for x in matrix.data[r][c]:
                        color = self.getSprite(x)
                        self.canvas.create_rectangle(
                            r * self.cellSize,
                            c * self.cellSize,
                            (r + 1) * self.cellSize,
                            (c + 1) * self.cellSize,
                            fill=color
                        )
                    pass

                color = self.getSprite(matrix.data[r][c])

                self.canvas.create_rectangle(
                    r * self.cellSize,
                    c * self.cellSize,
                    (r + 1) * self.cellSize,
                    (c + 1) * self.cellSize,
                    fill=color
                )
        return None

    def canvaClear(self):
        self.canvas.delete("all")

    def waitForClick(self):
        self._click_var = tk.IntVar()
        self._click_pos = None

        def on_click(event):
            col = event.x // self.cellSize
            row = event.y // self.cellSize
            self._click_pos = (row, col)
            self._click_var.set(1)  # unblock wait_variable

        self.canvas.bind("<Button-1>", on_click)

        # Wait until a click happens
        self.window.wait_variable(self._click_var)

        # Stop listening after click
        self.canvas.unbind("<Button-1>")

        return self._click_pos

    def run(self):
        self.window.mainloop()
