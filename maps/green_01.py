from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_shadows.png', tint=ika.RGB(255, 255, 255, 128)))
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 128)))
    #playMusic('island')



toGreen00 = exitTo('green_00.ika-map', 25, 5, 28)
toGreen02 = exitTo('green_02.ika-map', 14, 14, 1)
