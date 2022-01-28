
from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.bgThings.append(Clouds('gfx/sky_clouds.png', speed=(0.1, 0.025), tint=ika.RGB(255, 255, 255, 220)))           
    engine.mapThings.append(Clouds('gfx/sky_shadows.png', tint=ika.RGB(255, 5, 5, 255)))      
    #playMusic('island')

toGreen02 = exitTo('green_02.ika-map', 5, 19, 1, 'y')
toGreen07 = exitTo('green_07.ika-map', 5, 20, 38, 'y')
toGreen11 = exitTo('green_11.ika-map', 18, 18, 43)
toCave01 = exitTo('cave_01.ika-map', 48, 7, 27)
