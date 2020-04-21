from mapscript import *
from powerup import Grapple

class GrappleListener(Thing):
    def __init__(self):
        self.subject = None
        
    def update(self):
        
        if not self.subject:
            icon = Grapple(ika.Entity(64, 64, engine.player.ent.layer, "grappleicon.ika-sprite"))
            engine.addEntity(icon)
            self.subject = icon
            
        if self.subject not in engine.entities:
            return

def AutoExec():
    engine.background = ika.Image('gfx/dungeon_bg.png')
    if not 'grapple' in engine.saveData:
        engine.addThing(GrappleListener())
        
toTemple11 = exitTo('level1_11.ika-map', 22, 22, 3, 'y')
toTemple12 = exitTo('level1_12.ika-map', 22, 7, 35, 'y')
