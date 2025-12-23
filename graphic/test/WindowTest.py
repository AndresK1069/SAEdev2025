from tkinter import Grid

from graphic.Window import Window
from core.GridManager import GridManager
from core.Component.Wall import Wall

from core.Component.Grass import Grass

gm = GridManager(15)
g = Grass("D")
gm.getBattleZone(g)
testWindow = Window(600,"Mytest Window",15)
testWindow.renderMatrix(gm)

testWindow.run()