from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_shadows.png', tint=ika.RGB(255, 255, 255, 128)))
    #playMusic('island')

toGreen01 = exitTo('green_01.ika-map', 14, 14, 43)
toGreen03 = exitTo('green_03.ika-map', 3, 3, 1)
toGreen04 = exitTo('green_04.ika-map', 19, 5, 58, 'y')
