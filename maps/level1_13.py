from mapscript import *

def AutoExec():
    pass
    pos = []
    pos.append((10, 3, 'B2'))
    pos.append((10, 4, 'B2'))
    pos.append((39, 41, 'B2'))
    pos.append((39, 42, 'B2'))
    
    engine.mapThings.append(NoEnemyListener(pos, "level1_13_clear"))

toTemple12 = exitTo('level1_12.ika-map', 39, 19, 2)
toTemple14 = exitTo('level1_14.ika-map', 10, 9, 72)
