import tkinter as tk
from ctypes.wintypes import SIZEL

from core.GridManager import GridManager
from core.Component.Wall import Wall

from data.constante import SIZE, WINDOW_TITLE ,NCASES



#DRAWING background

grass = Wall("G")
test = GridManager(15)
test.getBattleZone(grass)


def on_click(event):
    coords.set((event.x, event.y))

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



#get click testes
coords = tk.Variable()
root.bind("<Button-1>", on_click)

print("Waiting for click...")
root.wait_variable(coords)

print("Clicked at:", coords.get())
x,y = coords.get()


def getCellInMatrix(x :int ,y :int):
    if isinstance(test.data[x][y],Wall):
        print("WALLLLL")




x= x//CELL_SIZE
y= y//CELL_SIZE


getCellInMatrix(x,y)


pos = tk.Variable()
x = pos.get()
print(x)



root.mainloop()

