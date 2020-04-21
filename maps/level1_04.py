from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/dungeon_bg.png')

toTemple03 = exitTo('level1_03.ika-map', 32, 52, 3)
toTemple05 = exitTo('level1_05.ika-map', 22, 7, 17, 'y')
toTemple06 = exitTo('level1_06.ika-map', 7, 7, 17, 'y')
toTemple08 = exitTo('level1_08.ika-map', 22, 7, 2, 'y')
toTemple09 = exitTo('level1_09.ika-map', 7, 7, 2, 'y')
