
import engine
import textbox
import dir

from entity import Entity
import controls

class Npc(Entity):
    '''Npcs are, specifically, non-combat entities.
    They are townspeople, merchants, and other folks who don't take damage,
    and may have something to say to the player.'''

    __non_anim = {}

    def __init__(self, ent, anim=None):
        super(Npc, self).__init__(ent, anim or self.__non_anim)

        self.invincible = True

        self.__touching = False

    def update(self):
        super(Npc, self).update()

        if self.touches(engine.player):
            if not self.__touching and (controls.attack1() or controls.joy_attack1()): #feels dirty to be checking controls here, but... 
                self.__touching = True
                self.__activate()
        else:
            self.__touching = False

    def __activate(self):
        p = engine.player
        p.state = p.defaultState()
        engine.tick()

        try:
            self.activate()
        finally:
            # Bump the player away, so he does not instantly activate the Npc again.
            #p = engine.player
            #d = dir.invert[p.direction]
            #deltaX, deltaY = dir.delta[d]
            #p.x += deltaX
            #p.y += deltaY

            engine.synchTime()

    def activate(self):
        func = getattr(engine.mapModule, self.ent.name)
        if func:
            func()
        else:
            print '<Npc.activate> What do I do?  I cannot find %s.%s and nobody thought to override me. ;_;' % (engine.mapName, self.ent.name)

    def text(self, *args):
        if len(args) == 1:
            txt = args[0]
            return textbox.text(self.ent, txt)
        elif len(args) == 2:
            portrait, txt = args
            return textbox.text(self.ent, portrait, txt)
