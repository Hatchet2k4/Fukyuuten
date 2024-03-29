from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.bgThings.append(Clouds('gfx/sky_clouds.png', speed=(0.1, 0.025), tint=ika.RGB(255, 255, 255, 220)))           
    engine.mapThings.append(ClippedClouds('stencils/green_02.ika-map.png', 'gfx/sky_shadows.png', tint=ika.RGB(255, 5, 5, 255)))      

toGreen01 = exitTo('green_01.ika-map', 14, 14, 43)
toGreen03 = exitTo('green_03.ika-map', 3, 3, 1)
toGreen04 = exitTo('green_04.ika-map', 19, 5, 58, 'y')
