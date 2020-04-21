from mapscript import *

def AutoExec():
    
    pos = []
    pos.append((31, 2, 'B2'))
    pos.append((31, 3, 'B2'))
    pos.append((31, 26, 'B2'))
    pos.append((31, 27, 'B2'))
    
    engine.mapThings.append(NoEnemyListener(pos, "cave_02_clear"))
    
toCave01 = exitTo('cave_01.ika-map', 31, 31, 3)
toCave03 = exitTo('cave_03.ika-map', 31, 13, 27)
