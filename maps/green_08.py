from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 96)))        

toGreen07 = exitTo('green_07.ika-map', 15, 15, 1)
toGreen09 = exitTo('green_09.ika-map', 2, 2, 38, 'y')
