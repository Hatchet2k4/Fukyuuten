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

from bee import createBee


_hiveAnim = {
    'walk': ((
        animator.makeAnim((4, 5), 3),
        animator.makeAnim((6, 7), 3),
        animator.makeAnim((2, 3), 3),
        animator.makeAnim((0, 1), 3),
        animator.makeAnim((4, 5), 3),
        animator.makeAnim((6, 7), 3),
        animator.makeAnim((4, 5), 3),
        animator.makeAnim((6, 7), 3),
        ),
        True
    ),

    'idle': ((
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),),
        ((0, 1000),)
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


def createHive(entity):
    return Hive(entity)


class Hive(Enemy):

    SPRITE = 'hive.ika-sprite'
    MAX_BEES = 6

    def __init__(self, ent):
        super(Hive, self).__init__(ent, _hiveAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        #self.addMoods(
        #    (Brain.Attack(1), self.attackMood),
        #    (Brain.Flee(1), self.passiveMood)
        #)

        self.mood = self.spawnMood

        self.beeCount = 0

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Hive, self).hurtState(0, recoilDir)

    def spawnMood(self):

        p = system.engine.player
        self._animator.kill = True
        while True:
            yield self.spawnState()
            yield self.idleState(500)


    def idleState(self, time=50):
        while time > 0:
            time -= 1
            self.anim = 'idle'
            yield None
        return

    def spawnState(self):
        if self.beeCount < self.MAX_BEES:
            bee_ent = ika.Entity(self.ent.x, self.ent.y, self.ent.layer, "bee.ika-sprite")
            engine.addEntity(createBee(bee_ent, self))
            self.beeCount += 1

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
