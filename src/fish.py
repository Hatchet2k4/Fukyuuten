
import ika
import engine
from entity import Entity

from npc import Npc

class Fish(Npc):
    SPRITE = 'fish.ika-sprite'

    def __init__(self, ent):
        super(Fish, self).__init__(ent, {})

    def activate(self):
        pass
