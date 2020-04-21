import ika
import math
import system
import Brain
import animator
import sound
import dir

from enemy import Enemy
from entity import Entity

_goblinAnim = {
    'walk': ((
        animator.makeAnim((4, 5), 10),
        animator.makeAnim((6, 7), 10),
        animator.makeAnim((2, 3), 10),
        animator.makeAnim((0, 1), 10),
        animator.makeAnim((4, 5), 10),
        animator.makeAnim((6, 7), 10),
        animator.makeAnim((4, 5), 10),
        animator.makeAnim((6, 7), 10),
        ),
        True
    ),

    'idle': ((
        ((4, 1000),),
        ((6, 1000),),
        ((2,  1000),),
        ((0,  1000),),
        ((4, 1000),),
        ((6, 1000),),
        ((4, 1000),),
        ((6, 1000),),
        ),
        True
    ),

    'attack': ((
        ((12, 30), (13, 15)),
        ((14, 30), (15, 15)),
        ((10, 30), (11, 15)),
        (( 8, 30), ( 9, 15)),
        ((12, 30), (13, 15)),
        ((14, 30), (15, 15)),
        ((12, 30), (13, 15)),
        ((14, 30), (15, 15)),
        ),
        False
    ),

    'bowattack': ((
        ((20, 50), (21, 30), (4, 1)),
        ((22, 50), (23, 30), (6, 1)),
        ((18, 50), (19, 30), (0, 1)),
        ((16, 50), (17, 30), (2, 1)),
        ((20, 50), (21, 30), (4, 1)),
        ((22, 50), (23, 30), (6, 1)),
        ((20, 50), (21, 30), (4, 1)),
        ((22, 50), (23, 30), (6, 1)),
        ),
        False
    ),

    'hurt': ((
        ((27, 1000),),
        ((26, 1000),),
        ((24, 1000),),
        ((25, 1000),),
        ((27, 1000),),
        ((26, 1000),),
        ((27, 1000),),
        ((26, 1000),),
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

_attackRange = [
    (-8,   0,  8, 16),
    (16,   0,  8, 16),
    ( 0, -8,  16,  8),
    ( 0,  16, 16,  8),
    (-8,   0,  8, 16),
    (16,   0,  8, 16),
    (-8,   0,  8, 16),
    (16,   0,  8, 16),
]


def createGoblin(entity):
    if entity.name.lower().startswith('archer'):
        return GoblinArcher(entity)
    else:
        return Goblin(entity)

def createUberGoblin(entity):
    if entity.name.lower().startswith('archer'):
        return UberGoblinArcher(entity)
    else:
        return UberGoblin(entity)

def createDesertGoblin(entity):
    if entity.name.lower().startswith('archer'):
        return DesertGoblinArcher(entity)
    else:
        return DesertGoblin(entity)


class Goblin(Enemy):

    SPRITE = 'goblin1.ika-sprite'

    def __init__(self, ent):
        super(Goblin, self).__init__(ent, _goblinAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        self.addMoods(
            (Brain.Attack(1), self.attackMood),
            (Brain.Flee(1), self.passiveMood)
        )

        self.mood = self.passiveMood

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        if self.stats.hp < self.stats.maxhp / 2:
            self.mood = self.fleeMood

        return super(Goblin, self).hurtState(recoilSpeed, recoilDir)

    def die(self, *args):
        """When one dies, the others come after the player."""

        ents = [
            system.engine.entFromEnt[x]
            for x in ika.EntitiesAt(self.x - 50, self.y - 50, 100, 100, self.layer)
            if x in system.engine.entFromEnt
        ]

        for a in ents:
            if not isinstance(a, Goblin) or a.stats.hp <= 0: continue

            a.mood = a.attackMood
            a.state = a.idleState()

        super(Goblin, self).die(*args)

    def attackMood(self):
        # if we want to be uber, we can remove this hack.
        # for now fuckit.  Attack the player!!

        p = system.engine.player
        for q in range(5):
            d = dir.fromDelta(p.x - self.x, p.y - self.y)
            dist = math.hypot(p.x - self.x, p.y - self.y)
            if dist < 40:
                yield self.attackState(d)
                yield self.idleState(40)
            else:
                yield self.walkState(d, min(30, dist))

    def fleeMood(self):
        MIN_DIST = 150
        p = system.engine.player
        for q in range(5):
            d = dir.fromDelta(p.x - self.x, p.y - self.y)
            dist = math.hypot(p.x - self.x, p.y - self.y)
            if dist > MIN_DIST:
                break
            yield self.walkState(dir.invert[d], MIN_DIST - dist)
        self.mood = self.passiveMood
        yield self.idleState()

    def passiveMood(self):
        p = system.engine.player
        self._animator.kill = True
        while True:
            dist = math.hypot(p.x - self.x, p.y - self.y)
            yield self.idleState()
            if dist < 150:
                self.mood = self.attackMood
                yield self.idleState()
                break

    def idleState(self, *args):
        self._animator.kill = True
        return super(Goblin, self).idleState(*args)

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
        self.speed *= 2

        # Winding up for the strike.  Stop until the animation advances to the
        # next frame.
        while self._animator.index == 0:
            yield None

        self.move(direction, 32)

        while not self._animator.kill:
            ents = self.detectCollision(_attackRange[direction])
            for e in ents:
                if e == system.engine.player:
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, self.direction)
                    yield None
                    return

            yield None

        self.stop()


class UberGoblin(Goblin):
    SPRITE = 'goblin2.ika-sprite'


class DesertGoblin(Goblin):
    SPRITE = 'goblin3.ika-sprite'


class Arrow(Entity):
    SPRITE = 'arrow.ika-sprite'

    ANIM = {
        'fly' : ((
            ((2, 1000),),
            ((3, 1000),),
            ((1, 1000),),
            ((0, 1000),),
            ((2, 1000),),
            ((3, 1000),),
            ((2, 1000),),
            ((3, 1000),),
        ), True),
    }

    def __init__(self, ent, direction, speed=250, damage=10, recoil=150):
        super(Arrow, self).__init__(ent, self.ANIM)

        self.direction = dir.straighten[direction]

        self.invincible = True
        self.speed = speed
        self.damage = damage
        self.recoil = recoil
        self.ent.isobs = False
        self.ent.entobs = False

    def defaultState(self):
        p = system.engine.player

        self.move(self.direction, 1000)
        assert self.direction in (dir.UP, dir.DOWN, dir.LEFT, dir.RIGHT)
        self.anim = 'fly'

        while True:

            ents = self.detectCollision((0, 0, 16, 16))
            for e in ents:
                if e is p:
                    p.hurt(self.damage, self.recoil, self.direction)
                    system.engine.destroyEntity(self)

            oldx = self.x
            oldy = self.y

            yield None

            if oldx == self.x and oldy == self.y:
                system.engine.destroyEntity(self)

class _Archer(object):
    '''Mixin class which overrides a goblin's attackMood and attackState
        so that it attacks with a bow instead of a knife.
    '''

    def attackMood(self):
        ATTACK_RANGE = 150

        p = system.engine.player

        def calcDist(pt):
            return math.hypot(pt[0] - self.x, pt[1] - self.y)

        oldx = self.x
        oldy = self.y
        curspot = None # sniping position to move to

        while True:

            # Archers are inexplicably only able to aim in the four cardinal directions.
            # That means there are four places the goblin wants to be.
            # (either directly above, below, or to the side of the player)
            # Find the closest one and head toward it.
            # If close enough to a happy spot, start shooting.

            if (self.x == oldx and self.y == oldy) or curspot is None:
                spots = (
                    (p.x, self.y),
                    (self.x, p.y),
                )

                dist = map(calcDist, spots)
                min_dist = min(dist)
                curspot = spots[dist.index(min(dist))]

            else:
                min_dist = calcDist(curspot)

            oldx = self.x
            oldy = self.y

            if min_dist <= 8:
                # FIXME: because of this, goblins will shoot diagonally.  Is this okay?
                d = dir.fromDelta(p.x - self.x, p.y - self.y)
                curspot = None
                yield self.attackState(d)
                yield self.idleState(60)

            else:
                d = dir.fromDelta(curspot[0] - self.x, curspot[1] - self.y)
                yield self.walkState(d, 8)

    def attackState(self, direction):
        self.direction = direction
        self.anim = 'bowattack'
        self.stop()

        # Windup time: wait for the first frame to finish showing
        while self._animator.index == 0:
            yield None

        # Spawn an arrow
        arrow = Arrow(ika.Entity(self.x, self.y, self.layer, 'arrow.ika-sprite'), direction)

        # compensate for rectangular hotspot blech.
        dx, dy = dir.delta[direction]
        if dx > 0: arrow.x += 16
        if dy <= 0: arrow.y -= 8

        system.engine.addEntity(arrow)

        # Stall
        i = 50
        while i > 0:
            i -= 1
            yield None

class GoblinArcher(Goblin, _Archer):
    attackMood = _Archer.attackMood
    attackState = _Archer.attackState

class DesertGoblinArcher(DesertGoblin, _Archer):
    attackMood = _Archer.attackMood
    attackState = _Archer.attackState


class UberGoblinArcher(UberGoblin, _Archer):
    attackMood = _Archer.attackMood
    attackState = _Archer.attackState
