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

_jellyAnim = {
    'walk': ((
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        ),
        True
    ),

    'grow': ((
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        animator.makeAnim((4, 5, 6, 7), 20),
        ),
        False
    ),
    
    'submerge': ((
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        animator.makeAnim((7, 6, 5, 4), 20),
        ),
        False
    ),    

    'idle': ((
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
        animator.makeAnim((0, 1, 2, 3), 20),
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


def createJelly(entity, pot=None):
    return Jelly(entity, pot)


class Jelly(Enemy):

    SPRITE = 'jelly.ika-sprite'
    MAX_SPLITS = 3

    def __init__(self, ent, pot=None):
        super(Jelly, self).__init__(ent, _jellyAnim, Brain.Brain())

        self.mood = self.growMood
        self.think()
        self.update()

        self.pot = pot

        self.speed = 20
        
        self.split = False
        self.splitTimes = 0

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Jelly, self).hurtState(recoilSpeed, recoilDir)

    def die(self, *args):
        if self.pot is not None and self.pot in engine.entities:
            self.pot.jellyCount -= 1
        super(Jelly, self).die(*args)


    def growMood(self):
        while True:
            yield self.growState()

    def passiveMood(self):

        p = system.engine.player
        self._animator.kill = True
        while True:
            yield self.walkState(ika.Random(0,8), ika.Random(24,64))
            yield self.idleState(ika.Random(0,20))
            if self.stats.hp <= self.stats.maxhp / 2 and self.splitTimes < self.MAX_SPLITS and not self.split:
                yield self.submergeState()
                yield self.splitState()
                yield self.growState()


    def idleState(self, *args):
        self._animator.kill = True
        return super(Jelly, self).idleState(*args)

    def growState(self):
        self.invincible = True
        self.anim = 'grow'
        self.ent.visible = True
        while not self._animator.kill:
            yield None
        self.invincible = False
        self.mood = self.passiveMood
        self.stop()
        
    def submergeState(self):
        self.invincible = True
        self.anim = 'submerge'
        while not self._animator.kill:
            yield None
        self.ent.visible = False
        self.stop()

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
                    self.stop()
                    break
            if (ox, oy) == (self.x, self.y):
                break
            yield None
        self.stop()

    def splitState(self):
            
        x = self.ent.x
        y = self.ent.y
        tw = ika.Tileset.width
        th = ika.Tileset.height
        
        pos = [(x-tw, y), (x, y-th), (x+tw, y), (x, y+th)]
        positions = []
        
        for n in pos:
            add = True
            for p in [(n[0], n[1]), (n[0]+tw-1, n[1]), (n[0], n[1]+th-1), (n[0]+tw-1, n[1]+th-1)]:
                if ika.Map.GetObs(p[0] / tw, p[1] / th, self.ent.layer):
                    add = False
                    break
            if add:
                positions.append(n)
        
        if positions:
            
            num = ika.Random(0, len(positions))
            p = positions[num]
            timer = 300
            
            while len(ika.EntitiesAt(p[0], p[1], tw, th, self.ent.layer)) > 1 and timer > 0:
                num = ika.Random(0, len(positions))
                p = positions[num]
                timer -= 1
                yield None
    
            if timer:
                jelly_ent = ika.Entity(p[0], p[1], self.ent.layer, "jelly.ika-sprite")
                new_jelly = createJelly(jelly_ent)
                new_jelly.splitTimes = self.splitTimes + 1
                new_jelly.stats.maxhp = self.stats.hp
                new_jelly.stats.hp = self.stats.hp
                engine.addEntity(new_jelly)
                
            self.split = True
        
        yield None

        self.stop()
