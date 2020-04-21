"""Contains entities that are obstructions in the player's path.
   Given the proper skill or item, the player can cross these.
"""

import ika
import engine
from caption import Caption
from entity import Entity


class Obstacle(Entity):

    def __init__(self, ent, anim=None):
        self.flagName = ent.name
        Entity.__init__(self, ent, anim)
        if 'beaten' in engine.saveData or self.flagName.startswith('secret'):
            if 'beaten' in engine.saveData:
                self.flagName += '2'
            split = self.ent.spritename.split('.')
            if 'beaten' in engine.saveData:
                self.ent.spritename = '%s%i.%s' % (split[0], engine.saveData['beaten'] + 1,
                                               split[1])
            else:
                self.ent.spritename = '%s%s.%s' % (split[0], self.flagName[6],
                                               split[1])
        self.invincible = True
        if self.flagName in engine.saveData:
            self.remove()

    def remove(self):
        self.x = self.y = -100  # hack!
        engine.destroyEntity(self)

    def update(self):
        pass


class IceWall(Obstacle):
    """Not very exciting.  The entity's type is all the information we
       need.
    """

    SPRITE = 'icecave.ika-sprite'
    SPRITE2 = 'ice.ika-sprite'


class Gap(Obstacle):
    """A big, empty hole."""

    SPRITE = 'vgap.ika-sprite'
    SPRITE2 = 'hgap.ika-sprite'
    SPRITE3 = 'sqgap.ika-sprite'


class IceChunks(Obstacle):

    SPRITE = 'icechunks.ika-sprite'

    _anim = {'default': ((((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),),
                          ((0, 50), (1, 50),)), True)}

    _frozenTiles = ((145, 149, 144),
                    (142, 113, 143),
                    (139, 148, 138))

    def __init__(self, ent):
        super(IceChunks, self).__init__(ent, self._anim)
        self.anim = 'default'

    def remove(self):
        self.freeze()
        super(IceChunks, self).remove()

    def freeze(self):
        lay = self.layer
        X = self.x / ika.Map.tilewidth
        Y = self.y / ika.Map.tileheight
        for y in range(3):
            for x in range(3):
                ika.Map.SetTile(x + X, y + Y, lay, self._frozenTiles[y][x])
                ika.Map.SetObs(x + X, y + Y, lay, False)
        engine.saveData[self.flagName] = 'True'


class Boulder(Obstacle):

    SPRITE = 'boulder.ika-sprite'

    def __init__(self, *args):
        Obstacle.__init__(self, *args)
        self.isTouching = False

    def update(self):
        t = self.touches(engine.player)
        if t and not self.isTouching:
            self.isTouching = True
            # find a stick of TNT
            lookfor = 'dynamite'
            if 'beaten' in engine.saveData:
                lookfor = 'c' + lookfor
            tnt = [k for k in engine.saveData
                     if k.startswith(lookfor) and
                        engine.saveData[k] == 'True']
            if tnt:
                # TODO: explode animation here
                engine.saveData[tnt[0]] = 'False'
                engine.saveData[self.flagName] = 'Broken'
                engine.destroyEntity(self)
                # change:
                engine.things.append(Caption('Blew the rock apart!'))
        else:
            self.isTouching = False
