import ika
import math
import system
import player
import Brain
import animator
import sound
import dir

from enemy import Enemy
from entity import Entity

_bugAnim = {
    'walk': ((
        animator.makeAnim((8, 9), 6),
        animator.makeAnim((10, 11), 6),
        animator.makeAnim((6, 7), 6),
        animator.makeAnim((4, 5), 6),
        animator.makeAnim((8, 9), 6),
        animator.makeAnim((10, 11), 6),
        animator.makeAnim((8, 9), 6),
        animator.makeAnim((10, 11), 6),
        ),
        True
    ),

    'idle': ((
        ((2, 1000),),
        ((3, 1000),),
        ((1,  1000),),
        ((0,  1000),),
        ((2, 1000),),
        ((3, 1000),),
        ((2, 1000),),
        ((3, 1000),),
        ),
        True
    ),

    'hurt': ((
        ((14, 1000),),
        ((15, 1000),),
        ((13, 1000),),
        ((12, 1000),),
        ((14, 1000),),
        ((15, 1000),),
        ((14, 1000),),
        ((15, 1000),),
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


def createBug(entity):
    return Bug(entity)


class Bug(Enemy):

    SPRITE = 'bug.ika-sprite'

    def __init__(self, ent):
        super(Bug, self).__init__(ent, _bugAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        #self.addMoods(
        #    (Brain.Attack(1), self.attackMood),
        #    (Brain.Flee(1), self.passiveMood)
        #)

        self.mood = self.passiveMood

        self.speed = 175

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        recoilSpeed = int(recoilSpeed * 1.5)

        return super(Bug, self).hurtState(recoilSpeed, recoilDir)

    def die(self, *args):
        super(Bug, self).die(*args)

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
            yield self.walkState(ika.Random(0,8), ika.Random(16,64))
            yield self.idleState(ika.Random(0,50))


    def idleState(self, *args):
        self._animator.kill = True
        return super(Bug, self).idleState(*args)

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
                    hurtDir = dir.fromDelta(e.x - self.x, e.y - self.y)
                    e.hurt(d, 150, hurtDir)
                    self.stop()
                    break
            if (ox, oy) == (self.x, self.y):
                break
            yield None                
        self.stop()
