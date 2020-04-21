import ika
import math
import system
import engine
import Brain
import animator
import sound
import dir

from enemy import Enemy
from entity import Entity

_frankenheadAnim = {
    'walk': ((
        animator.makeAnim((8, 9, 10, 11), 20),
        animator.makeAnim((12, 13, 14, 15), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((8, 9, 10, 11), 20),
        animator.makeAnim((12, 13, 14, 15), 20),
        animator.makeAnim((8, 9, 10, 11), 20),
        animator.makeAnim((12, 13, 14, 15), 20),
        ),
        True
    ),

    'idle': ((
        ((8,  1000),),
        ((12, 1000),),
        ((4,  1000),),
        ((0,  1000),),
        ((8,  1000),),
        ((12, 1000),),
        ((8,  1000),),
        ((12, 1000),),
        ),
        True
    ),

    'glow': ((
        animator.makeAnim((8, 18), 5),
        animator.makeAnim((12, 19), 5),
        animator.makeAnim((4, 17), 5),
        animator.makeAnim((0, 16), 5),
        animator.makeAnim((8, 18), 5),
        animator.makeAnim((12, 19), 5),
        animator.makeAnim((8, 18), 5),
        animator.makeAnim((12, 19), 5),
        ),
        True
    ),

    'hurt': ((
        ((22, 1000),),
        ((23, 1000),),
        ((21, 1000),),
        ((20, 1000),),
        ((22, 1000),),
        ((23, 1000),),
        ((22, 1000),),
        ((23, 1000),),
        ),
        False
    ),
}

def createFrankenhead(entity):
    return Frankenhead(entity)

class Frankenhead(Enemy):

    SPRITE = 'frankenhead.ika-sprite'

    def __init__(self, ent):
        super(Frankenhead, self).__init__(ent, _frankenheadAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        self.addMoods(
            (Brain.Flee(1), self.passiveMood)
        )

        self.mood = self.passiveMood

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Frankenhead, self).hurtState(recoilSpeed, recoilDir)

    def passiveMood(self):
        p = system.engine.player
        self._animator.kill = True
        while True:
            yield self.walkState(ika.Random(0,8), ika.Random(16,64))
            yield self.idleState(ika.Random(0,75))
            dist = math.hypot(p.x - self.x, p.y - self.y)
            if dist < 100:
                self.mood = self.summonMood
                yield self.idleState()
                break

    def summonMood(self):

        p = system.engine.player
        self._animator.kill = True

        while math.hypot(p.x - self.x, p.y - self.y) < 300:

            self.anim = 'glow'
            yield self.idleState(200)
            yield self.summonState()
            self._animator.kill = True
            yield self.idleState(200)
            break

        self.mood = self.passiveMood

    def idleState(self, time=50):
        while time > 0:
            time -= 1
            yield None
        return

    def walkState(self, dir, dist):
        ox, oy = self.x, self.y
        self.move(dir, dist)
        self.anim = 'walk'
        yield None
        while self.moving:
            yield None
            if (ox, oy) == (self.x, self.y):
                break
        self.stop()

    def summonState(self):
        self.anim = 'glow'
        p = engine.player
        for b in range(6):
            xr = ika.Random(-24, 24)
            yr = ika.Random(-24, 24)
            engine.addEntity(Bone(ika.Entity(p.x + xr, p.y + yr - 300, ika.Map.layercount-1, 'frankenhead_bone.ika-sprite')))
            for x in range(15):
                yield None
        yield None
        self.stop()


class Bone(Entity):
    SPRITE = 'frankenhead_bone.ika-sprite'

    ANIM = {
        'twirl' : ((
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
            animator.makeAnim(range(0,4), 10),
        ), True),

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

    def __init__(self, ent, speed=175, damage=10, recoil=250):
        super(Bone, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.speed = speed
        self.damage = damage
        self.recoil = recoil
        self.ent.mapobs = False
        self.ent.entobs = False
        self.ent.isobs = False

        self.state = self.defaultState()

    def defaultState(self):

        p = engine.player

        destY = self.y + 300

        engine.addEntity(BoneShadow(ika.Entity(self.x, destY, p.ent.layer, 'frankenhead_shadow.ika-sprite'), self))

        self.anim = 'twirl'

        self.move(dir.DOWN, 100000)
        while self.y < destY:
            yield None
        self.stop()

        self.speed = 0

        self.ent.spritename = 'frankenhead_explode.ika-sprite'
        self.anim = 'explode'
        self.x -= 12
        self.y -= 12

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

class BoneShadow(Entity):
    SPRITE = 'frankenhead_shadow.ika-sprite'

    ANIM = {}

    def __init__(self, ent, creator):
        super(BoneShadow, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.ent.mapobs = False
        self.ent.entobs = False
        self.ent.isobs = False

        self.creator = creator

        self.state = self.defaultState()

    def defaultState(self):

        while self.creator.ent.spritename == 'frankenhead_bone.ika-sprite':
            dist = self.y - self.creator.y
            self.ent.specframe = 3 - (dist * 3 / 300)
            yield None

        engine.destroyEntity(self)

        while True:
            yield None
