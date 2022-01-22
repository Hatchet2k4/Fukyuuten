from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 96)))        

toGreen08 = exitTo('green_08.ika-map', 2, 2, 1, 'y')
toGreen10 = exitTo('green_10.ika-map', 25, 25, 1)
