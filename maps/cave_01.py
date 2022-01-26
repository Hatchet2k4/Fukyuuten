from mapscript import *

def AutoExec():
    pass
    #engine.background = ika.Image('gfx/sky_bg.png')
    #playMusic('dungeon')
    pos = []
    pos.append((31, 2, 'B2'))
    pos.append((31, 3, 'B2'))    
    engine.mapThings.append(NoEnemyListener(pos, "cave_01_clear"))
    
toGreen04 = exitTo('green_04.ika-map', 7, 48, 5)
toCave02 = exitTo('cave_02.ika-map', 31, 31, 26)
