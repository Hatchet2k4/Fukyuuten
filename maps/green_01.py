from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.bgThings.append(Clouds('gfx/sky_clouds.png', speed=(0.1, 0.025), tint=ika.RGB(255, 255, 255, 220)))           
    engine.mapThings.append(ClippedClouds('stencils/green_01.ika-map.png', 'gfx/sky_shadows.png', tint=ika.RGB(255, 5, 5, 255)))          

toGreen00 = exitTo('green_00.ika-map', 25, 5, 28)
toGreen02 = exitTo('green_02.ika-map', 14, 14, 1)
