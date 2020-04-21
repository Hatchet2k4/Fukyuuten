import ika
import math
import system
import player
import Brain
import animator
import sound
import dir

import engine

from enemy import Enemy
from entity import Entity

#from tentacle import createTentacle


_plantAnim = {

    'idle': ((
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        animator.makeAnim((0, 1, 2, 1), 20),
        ),
        True
    ),

    'hurt': ((
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ((4, 1000),),
        ),
        False
    ),

    'die': ((
        ((38, 20), (39, 90)),
        ((33, 20), (34, 90)),
        ((23, 20), (24, 90)),
        ((28, 20), (29, 90)),
        ((38, 20), (39, 90)),
        ((33, 20), (34, 90)),
        ((38, 20), (39, 90)),
        ((33, 20), (34, 90)),
        ),
        False
    ),
}


def createPlant(entity):
    return Plant(entity)


class Plant(Enemy):

    SPRITE = 'plant.ika-sprite'

    def __init__(self, ent):
        super(Plant, self).__init__(ent, _plantAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        #self.addMoods(
        #    (Brain.Attack(1), self.attackMood),
        #    (Brain.Flee(1), self.passiveMood)
        #)

        self.mood = self.spawnMood

        self.last = None

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Plant, self).hurtState(0, recoilDir)

    def spawnMood(self):

        p = system.engine.player
        self._animator.kill = True
        last = None

        while True:

            dist = math.hypot(p.x - self.x, p.y - self.y)

            if dist < 80:
                if not last or last == 'spore':
                    last = 'tentacle'
                    for x in range(3):
                        yield self.spawnTentacleState()
                        yield self.idleState(50)
                    yield self.idleState(300 - self.desperation)
                else:
                    last = 'spore'
                    for x in range(2):
                        yield self.spawnSporeState()
                        yield self.idleState(75)
                    yield self.idleState(300 - self.desperation)

            elif dist < 200:
                last = 'spore'
                for x in range(3):
                    yield self.spawnSporeState()
                    yield self.idleState(150)
                yield self.idleState(400 - self.desperation)

            yield self.idleState(20)


    def idleState(self, *args):
        self._animator.kill = True
        return super(Plant, self).idleState(*args)

    def spawnTentacleState(self):
        p = engine.player
        engine.addEntity(Tentacle(ika.Entity(p.x, p.y, self.layer, 'plant_tentacle.ika-sprite'), self))
        yield None
        self.stop()

    def spawnSporeState(self):
        x = self.x + self.ent.hotwidth / 2 - 4
        y = self.y + self.ent.hotheight / 2 - 4
        engine.addEntity(Spore(ika.Entity(x, y, ika.Map.layercount-1, 'plant_spore.ika-sprite')))
        yield None
        self.stop()

    def hurt(self, amount, recoilSpeed=0, recoilDir=None):
        if self.invincible:
            return
        if recoilDir is None:
            recoilDir = dir.invert[self.direction]
        if self.stats.hp <= amount:
            self.stats.hp = 0
            self.die()
        else:
            self.stats.hp -= amount

    desperation = property(lambda self: int(100 - (self.stats.maxhp * 100.0 / self.stats.hp)))

class Tentacle(Entity):
    SPRITE = 'plant_tentacle.ika-sprite'

    ANIM = {
        'grow' : ((
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
            animator.makeAnim((0, 1), 40),
        ), False),

        'die' : ((
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
            animator.makeAnim((2, 3, 4), 40),
        ), False),
    }

    def __init__(self, ent, creator, speed=100, damage=7, recoil=200):
        super(Tentacle, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.speed = speed
        self.damage = damage
        self.recoil = recoil
        self.ent.isobs = False
        self.ent.entobs = False

        self.creator = creator
        self.check = True

        self.state = self.defaultState()

        self.hit = False

    def defaultState(self):
        p = system.engine.player
        self.anim = 'grow'

        while not self._animator.kill:
            if not self.creator:
                self.check = False
                break
            yield None

        self.anim = 'die'
        yield None

        while not self._animator.kill:

            if self.ent.specframe == 3 and self.creator in engine.entities:

                if not self.hit and self.check:
                    ents = self.detectCollision((0, 0, self.ent.hotwidth, self.ent.hotheight))
                    for e in ents:
                        if e is p:
                            p.hurt(self.damage, self.recoil, dir.fromDelta(self.creator.x - p.x, self.creator.y - p.y))
                            self.hit = True

            yield None

        engine.destroyEntity(self)

class Spore(Entity):
    SPRITE = 'plant_spore.ika-sprite'

    ANIM = {
        'explode' : ((
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
            animator.makeAnim(range(0,6), 10),
        ), False),
    }

    def __init__(self, ent, speed=200, damage=14, recoil=200):
        super(Spore, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.speed = speed
        self.damage = damage
        self.recoil = recoil
        self.ent.mapobs = False
        self.ent.entobs = False
        self.ent.isobs = False

        self.state = self.defaultState()

    def defaultState(self):

        p = system.engine.player

        self.move(dir.UP, 100000)
        while self.y > -10:
            yield None
        self.stop()

        for x in range(100):
            yield None

        self.x = p.x + p.ent.hotwidth / 2 - 4
        destY = p.y + p.ent.hotheight / 2 - 4

        self.y = p.y - 300

        engine.addEntity(SporeShadow(ika.Entity(self.x, destY, p.ent.layer, 'plant_shadow.ika-sprite'), self))

        self.move(dir.DOWN, 100000)
        sound.fall.Play()
        while self.y < destY:
            yield None
        self.stop()

        sound.sporeHit.Play()
        
        self.speed = 0

        self.ent.spritename = 'plant_explode.ika-sprite'
        self.anim = 'explode'
        self.x -= 12
        self.y -= 12

        sound.sporeHit.Play()
        
        oldLayer = self.ent.layer
        self.ent.layer = p.ent.layer
        ents = self.detectCollision((0, 0, self.ent.hotwidth, self.ent.hotheight))
        self.ent.layer = oldLayer

        for e in ents:
            if e is p:
                p.hurt(self.damage, self.recoil, ika.Random(0,8))

        while not self._animator.kill:
            yield None

        engine.destroyEntity(self)

        while True:
            yield None

class SporeShadow(Entity):
    SPRITE = 'plant_shadow.ika-sprite'

    ANIM = {}

    def __init__(self, ent, creator):
        super(SporeShadow, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.ent.mapobs = False
        self.ent.entobs = False
        self.ent.isobs = False

        self.creator = creator

        self.state = self.defaultState()

    def defaultState(self):

        while self.creator.ent.spritename == 'plant_spore.ika-sprite':
            dist = self.y - self.creator.y
            self.ent.specframe = 3 - (dist * 3 / 300)
            yield None

        engine.destroyEntity(self)

        while True:
            yield None
