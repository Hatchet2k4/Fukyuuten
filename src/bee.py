import ika
import math
import system
import engine
import player
import Brain
import animator
import sound
import dir

from enemy import Enemy
from entity import Entity

_beeAnim = {
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


def createBee(entity, hive=None):
    return Bee(entity, hive)


class Bee(Enemy):

    SPRITE = 'bee.ika-sprite'

    def __init__(self, ent, hive=None):
        super(Bee, self).__init__(ent, _beeAnim, Brain.Brain())
        self.ent.mapobs = False
        self.ent.entobs = False

        self.hive = hive
        self.mood = self.passiveMood

        self.speed = 125

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Bee, self).hurtState(recoilSpeed, recoilDir)

    def die(self, *args):
        if self.hive is not None and self.hive in engine.entities:
            self.hive.beeCount -= 1

        super(Bee, self).die(*args)

    def passiveMood(self):

        p = system.engine.player
        self._animator.kill = True
        while True:
            yield self.walkState(ika.Random(0,8), ika.Random(8,32))

            tx = (self.ent.x + self.ent.hotwidth) / ika.Tileset.width
            ty = (self.ent.y + self.ent.hotheight) / ika.Tileset.height

            # if on a flower, sit there
            if ika.Map.GetTile(tx, ty, self.ent.layer) in [356, 357, 358, 364, 365, 366]:
                yield self.idleState(400)
            else:
                yield self.idleState(ika.Random(0,10))


    def idleState(self, *args):
        self._animator.kill = True
        return super(Bee, self).idleState(*args)

    def walkState(self, direction, dist):
        ox, oy = self.x, self.y
        self.move(direction, dist)
        self.anim = 'walk'
        yield None
        while self.moving:
            ents = self.detectCollision((0, 0, self.ent.hotwidth, self.ent.hotheight))
            for e in ents:
                if isinstance(e, player.Player):
                    d = max(1, self.stats.att - e.stats.pres)
                    e.hurt(d, 150, dir.fromDelta(e.x - ox, e.y - oy))
                    break
            if (ox, oy) == (self.x, self.y):
                break
            yield None
        self.stop()
