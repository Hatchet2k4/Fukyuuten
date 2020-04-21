from mapscript import *
from maneater import Maneater
import engine

class DeathListener(Thing):
    def __init__(self):
        self.subject = None
        
    def update(self):
        
        if not self.subject:
            boss = Maneater(ika.Entity(136, 96, engine.player.ent.layer, "maneater.ika-sprite"))
            engine.addEntity(boss)
            self.subject = boss
    
            # Close the way in
            ika.Map.SetTile(9, 16, engine.player.ent.layer, 182)
            ika.Map.SetTile(9, 17, engine.player.ent.layer, 190)
            ika.Map.SetTile(16, 8, engine.player.ent.layer, 167)
            ika.Map.SetTile(16, 9, engine.player.ent.layer, 175)
            ika.Map.SetObs(16, 9, engine.player.ent.layer, True)
            ika.Map.SetObs(9, 17, engine.player.ent.layer, True)
            
        if self.subject not in engine.entities:
            self.bossDied()
            engine.saveData['maneater'] = True
            return True

    def bossDied(self):
        # Open the path forward
        ika.Map.SetTile(9, 16, engine.player.ent.layer, 0)
        ika.Map.SetTile(9, 17, engine.player.ent.layer, 0)
        ika.Map.SetTile(16, 8, engine.player.ent.layer, 0)
        ika.Map.SetTile(16, 9, engine.player.ent.layer, 0)
        ika.Map.SetObs(16, 9, engine.player.ent.layer, False)
        ika.Map.SetObs(9, 17, engine.player.ent.layer, False)
        
        
def AutoExec():
    playMusic('boss')
    
    if 'maneater' not in engine.saveData:
        engine.mapThings.append(DeathListener())

toTemple14 = exitTo('level1_14.ika-map', 9, 9, 3)
toTemple16 = exitTo('level1_16.ika-map', 9, 9, 2, 'y')
