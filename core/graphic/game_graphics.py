import tkinter as tk
from ctypes.wintypes import SIZEL

from core.GridManager import GridManager
from core.Component.Wall import Wall

from data.constante import SIZE, WINDOW_TITLE ,NCASES



#DRAWING background

grass = Wall("G")
test = GridManager(15)
test.getBattleZone(grass)




if SIZE%3 !=0:
    raise ValueError("WIDTH must be divisible by 3")
CELL_SIZE=SIZE// NCASES


#Window prototype
root = tk.Tk()
canvas = tk.Canvas(root, width=SIZE, height=SIZE,)
canvas.pack()
root.title(WINDOW_TITLE)

for r in range(len(test.data)):
    for c in range(len(test.data)):

        if isinstance(test.data[r][c],Wall):
            canvas.create_rectangle(
                r*CELL_SIZE,
                c*CELL_SIZE,
                (r+1)*CELL_SIZE,
                (c+1)*CELL_SIZE,
                fill="green"
            )
        if test.data[r][c] is None:
            canvas.create_rectangle(
                r*CELL_SIZE,
                c*CELL_SIZE,
                (r+1)*CELL_SIZE,
                (c+1)*CELL_SIZE,
                fill="SpringGreen2"
            )


root.mainloop()

