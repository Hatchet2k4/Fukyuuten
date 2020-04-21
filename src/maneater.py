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
from powerup import RedBerry, Seashell
from quake import Quake


_maneaterAnim = {

    'idle': ((
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ),
        False
    ),

    'wait_in': ((
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        animator.makeAnim((7, 6, 5, 6), 20),
        ),
        True
    ),

    'wait_out': ((
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        animator.makeAnim((12, 13, 14, 15, 14, 13), 20),
        ),
        True
    ),

    'grow': ((
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        animator.makeAnim((0, 1, 2, 3, 7), 20),
        ),
        False
    ),

    'submerge': ((
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        animator.makeAnim((7, 3, 2, 1, 0), 10),
        ),
        False
    ),

    'show': ((
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        animator.makeAnim((7, 8, 9, 10, 11), 20),
        ),
        False
    ),

    'hide': ((
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        animator.makeAnim((16, 11, 10, 9, 8), 20),
        ),
        False
    ),

    'spawnspears': ((
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ((7, 1000),),
        ),
        True
    ),

    'spawnspores': ((
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
        animator.makeAnim((5, 4), 20),
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


class Maneater(Enemy):

    SPRITE = 'maneater.ika-sprite'

    def __init__(self, ent):
        super(Maneater, self).__init__(ent, _maneaterAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        #self.addMoods(
        #    (Brain.Attack(1), self.attackMood),
        #    (Brain.Flee(1), self.passiveMood)
        #)

        self.stats.hp = 2
        self.stats.maxhp = 2
        self.mood = self.growMood
        self.invincible = True

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Maneater, self).hurtState(0, recoilDir)


    def growMood(self):
        engine.addThing(Quake(duration=25, x=8, y=8))
        yield self.growState()
        self.mood = self.spawnMood
        yield self.passiveState()


    def spawnMood(self):
        p = system.engine.player
        self.anim = 'wait_in'
        while True:

            # ---- PHASE 1 - Spores ---- #

            self.anim = 'spawnspores'
            yield self.idleState(100)

            for r in range(4):
                engine.addThing(Quake(duration=50, x=5, y=5))
                yield self.spawnSporeState(7-r)
                while self.numSpores:
                    yield self.idleState()

            self.anim = 'wait_in'
            yield self.idleState(200)

            # ---- PHASE 2 - Spears ---- #

            self.anim = 'spawnspears'
            yield self.idleState(100)

            for r in range(8):
                yield self.spawnSpearState()
                engine.addThing(Quake(duration=25, x=10, y=10))
                while self.numSpears:
                    yield self.idleState()
                yield self.idleState(10)

            self.anim = 'wait_in'
            yield self.idleState(500)

            # ---- PHASE 3 - Summon Tentacles ---- #

            yield self.submergeState()

            engine.addThing(Quake(duration=150, x=4, y=4))
            yield self.spawnTentacleState()

            self.anim = 'idle'
            yield self.idleState(100)

            # ---- PHASE 4 - Wait ---- #

            yield self.passiveState()

            # ---- PHASE 5 - Show ---- #

            yield self.growState()
            yield self.showState()
            yield self.idleState(1000)
            yield self.hideState()

            # ---- PHASE 6 - Warmup ---- #

            yield self.idleState(400)



    def growState(self):
        sound.maneaterHead.Play()
        self.anim = 'grow'
        while not self._animator.kill:
            yield None

    def submergeState(self):
        sound.maneaterHead.Play()
        self.anim = 'submerge'
        while not self._animator.kill:
            yield None

    def showState(self):
        self.anim = 'show'
        while not self._animator.kill:
            yield None
        self.invincible = False
        self.anim = 'wait_out'


    def hideState(self):
        self.anim = 'hide'
        self.invincible = True
        while not self._animator.kill:
            yield None
        self.anim = 'wait_in'


    def passiveState(self, *args):
        while True:
            if not self.numTentacles:
                break
            yield None
        yield None


    def idleState(self, time=50):
        while time > 0:
            time -= 1
            yield None
        return


    def spawnSpearState(self, mode=0):

        p = engine.player

        # MODE 1 -- random spears
        if mode == 0:

            rngX = range(3, 15, 4)
            rngY = range(4, 16, 4)

            for rx in rngX:
                for ry in rngY:
                    x = rx * ika.Tileset.width + ika.Random(0, ika.Tileset.width * 4)
                    y = ry * ika.Tileset.height + ika.Random(0, ika.Tileset.height * 4)
                    engine.addEntity(ManeaterSpear(ika.Entity(x, y, self.layer, 'plant_tentacle.ika-sprite'), self))

            engine.addEntity(ManeaterSpear(ika.Entity(p.x, p.y, self.layer, 'plant_tentacle.ika-sprite'), self))

        yield None


    def spawnSporeState(self, freq=7):

        cx = 9.5 * ika.Tileset.width
        cy = 10.5 * ika.Tileset.height
        rad = ika.Tileset.width * 7
        cosDeg = lambda n: math.cos(n*math.pi/180.0)
        sinDeg = lambda n: math.sin(n*math.pi/180.0)

        forRange = lambda: range(0, 360, 90 / (rad / ika.Tileset.width))
        backRange = lambda: range(360, 0, -90 / (rad / ika.Tileset.width))
        ranges = [forRange, backRange]
        pos = 0

        mode = ika.Random(0,2)  # 2 different modes
        
        # MODE 1 - closing circles
        if mode == 0:

            while rad > 0:
                
                cnt = 0
                sound.fall.Play()
                play = True
                rng = ranges[pos]()
                for deg in rng:
                    x = cx + cosDeg(deg) * rad - 4
                    y = cy + sinDeg(deg) * rad - 4
                    engine.addEntity(ManeaterSpore(ika.Entity(x, y, ika.Map.layercount-1, 'maneater_spore.ika-sprite'), play=play))
                    for time in range(2):
                        yield None
                    if play:
                        play = False
                    elif cnt < 4:
                        cnt += 1
                    else:
                        cnt = 0
                        play = True
                pos ^= 1
                for time in range(40):
                    yield None
                rad -= ika.Tileset.width * 2

                engine.addThing(Quake(duration=25, x=10, y=10))

        # MODE 2 - random bombardment
        elif mode == 1:

            rng = ranges[0]()
            
            sound.fall.Play()
            
            play = True
            while rad > 0:
                for deg in rng:
                    if not ika.Random(0,freq):  # half chance of bombarding this one
                        x = cx + cosDeg(deg) * rad - 4
                        y = cy + sinDeg(deg) * rad - 4
                        engine.addEntity(ManeaterSpore(ika.Entity(x, y, ika.Map.layercount-1, 'maneater_spore.ika-sprite'), play=play))
                        play = False
                rad -= ika.Tileset.width

        yield None

    def spawnTentacleState(self):

        p = engine.player

        yp = [7.5, 10.5, 13.5]
        xp = [4.5, 12.5]
        comb = []

        order = []

        for y in yp:
            for x in xp:
                comb.append((x,y))

        for n in range(len(comb)):
            a = ika.Random(0,len(comb))
            order.append(comb[a])
            comb.pop(a)

        for x,y in order:
            t = ManeaterTentacle(ika.Entity(int(x * ika.Tileset.width), int(y * ika.Tileset.height), self.layer, 'maneater_tentacle.ika-sprite'), self)
            t.direction = [dir.RIGHT, dir.LEFT][int(x)/10]
            engine.addEntity(t)
            sound.maneaterTentacle.Play()

            for time in range(25):
                yield None

        yield None
        self.stop()

    def deathState(self, *args, **kwargs):
        sound.maneaterDie.Play()
        self.anim = 'die'
        return super(Maneater, self).deathState(*args, **kwargs)

    def hurt(self, amount, recoilSpeed=0, recoilDir=None):
        p = engine.player
        if self.invincible:
            engine.addThing(Quake(duration=25, x=50, y=50))
            p.recoil(175, dir.invert[p.direction])
            return
        else:
            engine.addThing(Quake(duration=100, x=30, y=30))
        if recoilDir is None:
            recoilDir = dir.invert[self.direction]
        if self.stats.hp <= 1:
            self.stats.hp = 0
            self.die()
            p.recoil(175, dir.invert[p.direction])
        else:
            sound.maneaterHit.Play()
            super(Maneater, self).hurt(1, recoilSpeed, recoilDir)

    numSpears = property(lambda self: len([e for e in engine.entities if isinstance(e, ManeaterSpear)]))
    numSpores = property(lambda self: len([e for e in engine.entities if isinstance(e, ManeaterSpore)]))
    numTentacles = property(lambda self: len([e for e in engine.entities if isinstance(e, ManeaterTentacle)]))


class ManeaterSpear(Entity):
    SPRITE = 'plant_tentacle.ika-sprite'

    ANIM = {
        'grow' : ((
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
        ), False),

        'die' : ((
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
            animator.makeAnim((2, 3, 4), 20),
        ), False),
    }

    def __init__(self, ent, creator, speed=100, damage=15, recoil=250):
        super(ManeaterSpear, self).__init__(ent, self.ANIM)

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


class ManeaterSpore(Entity):
    SPRITE = 'maneater_spore.ika-sprite'

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

    def __init__(self, ent, speed=200, damage=5, recoil=350, play=True):
        super(ManeaterSpore, self).__init__(ent, self.ANIM)

        self.invincible = True
        self.speed = speed
        self.damage = damage
        self.recoil = recoil
        self.play = play
        self.ent.mapobs = False
        self.ent.entobs = False
        self.ent.isobs = False

        self.state = self.defaultState()

    def defaultState(self):

        p = system.engine.player

        destY = self.y
        self.y -= 300

        engine.addEntity(SporeShadow(ika.Entity(self.x, destY, p.ent.layer, 'maneater_shadow.ika-sprite'), self))

        self.move(dir.DOWN, 100000)
        while self.y < destY:
            yield None
        self.stop()

        if self.play:
            sound.sporeHit.Play()
            
        self.speed = 0

        self.ent.spritename = 'maneater_explode.ika-sprite'
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

class SporeShadow(Entity):
    SPRITE = 'maneater_shadow.ika-sprite'

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

        while self.creator.ent.spritename == 'maneater_spore.ika-sprite':
            dist = self.y - self.creator.y
            self.ent.specframe = 3 - (dist * 3 / 300)
            yield None

        engine.destroyEntity(self)

        while True:
            yield None


class ManeaterTentacle(Enemy):
    SPRITE = 'maneater_tentacle.ika-sprite'

    ANIM = {

        'idle' : ((
            animator.makeAnim((10, 11), 20),
            animator.makeAnim((6, 7), 20),
            animator.makeAnim((10, 11), 20),
            animator.makeAnim((6, 7), 20),
            animator.makeAnim((10, 11), 20),
            animator.makeAnim((6, 7), 20),
            animator.makeAnim((10, 11), 20),
            animator.makeAnim((6, 7), 20),
        ), True),

        'grow' : ((
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
            animator.makeAnim((0, 1, 2, 3), 10),
        ), False),

        'submerge' : ((
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
        ), False),

        'attack' : ((
            animator.makeAnim((16, 17), 20),
            animator.makeAnim((18, 19), 20),
            animator.makeAnim((13, 14), 20),
            animator.makeAnim((11, 12), 20),
            animator.makeAnim((16, 17), 20),
            animator.makeAnim((18, 19), 20),
            animator.makeAnim((16, 17), 20),
            animator.makeAnim((18, 19), 20),
        ), False),

        'hurt' : ((
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
            animator.makeAnim((20, 21, 22, 23), 10),
        ), False),

    }

    ATKRANGE = [
        (-8,   0,  8, 16),
        (16,   0,  8, 16),
        ( 0, -8,  16,  8),
        ( 0,  16, 16,  8),
        (-8,   0,  8, 16),
        (16,   0,  8, 16),
        (-8,   0,  8, 16),
        (16,   0,  8, 16)
    ]

    def __init__(self, ent, creator):
        super(ManeaterTentacle, self).__init__(ent, self.ANIM, Brain.Brain())

        self.speed = 0

        # Test code:
        # Equal probability of attacking or doing nothing.
        self.addMoods(
            (Brain.Attack(1), self.attackMood),
        )

        self.stats.maxhp = self.stats.hp = 60
        self.stats.att = 25
        self.stats.exp = 0

        self.stats.money = 0



        self.recoil = 200
        self.ent.isobs = False
        self.ent.entobs = False
        self.creator = creator
        self.mood = self.attackMood
        self.state = self.growState()
        self.powerup = RedBerry
        self.hit = False

    def attackMood(self):

        p = engine.player

        self.anim = 'idle'

        cnt = 0

        while True:
            dist = math.hypot(p.x - self.x, p.y - self.y)

            if dist < 40:
                yield self.attackState(dir.fromDelta(p.x - self.x, p.y - self.y))

            if cnt >= 500:
                self.mood = self.submergeMood
                yield self.idleState()
                break
            else:
                cnt += 1

            yield self.idleState(1)


    def submergeMood(self):

        p = engine.player

        yield self.submergeState()
        yield self.idleState(150)

        while True:
            dist = math.hypot(p.x - self.x, p.y - self.y)

            if dist > 100:
                yield self.growState()
                self.mood = self.attackMood
                break

            elif dist < 20:
                d = max(1, self.stats.att - p.stats.pres)
                p.hurt(d, self.recoil, self.direction)
                yield self.growState()
                self.mood = self.attackMood
                yield self.idleState()
                break

            else:
                engine.addEntity(ManeaterSpear(ika.Entity(p.x - 8, p.y - 8, self.layer, 'plant_tentacle.ika-sprite'), self))
                yield self.idleState(60)

            yield self.idleState()


    def growState(self):
        sound.maneaterHead.Play()
        ents = self.detectCollision([0, 0, self.ent.hotwidth, self.ent.hotheight])
        while len(ents) > 1:
            ents = self.detectCollision([0, 0, self.ent.hotwidth, self.ent.hotheight])
            yield None
        self.anim = 'grow'
        self.ent.isobs = True
        self.invincible = False
        self.hit = False
        while not self._animator.kill:
            yield None
        yield None

    def submergeState(self):
        sound.maneaterHead.Play()
        self.anim = 'submerge'
        self.ent.isobs = False
        self.invincible = True
        while not self._animator.kill:
            yield None
        yield None


    def attackState(self, direction):
        class SpeedSaver(object):
            def __init__(_self):
                _self.s = self.speed
            def __del__(_self):
                self.speed = _self.s
        ss = SpeedSaver()

        self.direction = direction
        self.anim = 'attack'
        self.stop()

        while self._animator.index == 0:
            yield None

        sound.tentacleStrike.Play()

        while not self._animator.kill:

            ents = self.detectCollision([-8, -8, self.ent.hotwidth + 16, self.ent.hotheight + 16])
            for e in ents:
                if e == engine.player and not self.hit:
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, self.recoil, self.direction)
                    self.hit = True

            yield None

        self.hit = False
        self.anim = 'idle'

        yield None

        self.stop()


    def hurtState(self, recoilSpeed, recoilDir):

        if self.stats.hp > 0:
            sound.enemyHit.Play()

        self.mood = self.submergeMood

        return super(ManeaterTentacle, self).hurtState(0, recoilDir)

    def idleState(self, time=50):
        while time > 0:
            time -= 1
            yield None
        return
