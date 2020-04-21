
from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    playMusic('island')

toGreen02 = exitTo('green_02.ika-map', 5, 19, 1, 'y')
toGreen07 = exitTo('green_07.ika-map', 5, 20, 38, 'y')
toGreen11 = exitTo('green_11.ika-map', 18, 18, 43)
toCave01 = exitTo('cave_01.ika-map', 48, 7, 27)
