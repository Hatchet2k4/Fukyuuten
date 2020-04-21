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

from jelly import createJelly


_potAnim = {

    'idle': ((
        ((3, 1000),),
        ((2, 1000),),
        ((1, 1000),),
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
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
        ((3, 1000),),
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


def createPot(entity):
    return Pot(entity)


class Pot(Enemy):

    SPRITE = 'pot.ika-sprite'
    MAX_JELLIES = 12

    def __init__(self, ent):
        super(Pot, self).__init__(ent, _potAnim, Brain.Brain())

        # Test code:
        # Equal probability of attacking or doing nothing.
        #self.addMoods(
        #    (Brain.Attack(1), self.attackMood),
        #    (Brain.Flee(1), self.passiveMood)
        #)

        self.mood = self.spawnMood

        self.direction = dir.DOWN
        self.divisor = self.stats.maxhp / 4
        self.jellyCount = 0

    def hurtState(self, recoilSpeed, recoilDir):
        if self.stats.hp > 0:
            sound.enemyHit.Play()

        return super(Pot, self).hurtState(0, recoilDir)

    def spawnMood(self):

        p = system.engine.player
        self._animator.kill = True
        while True:
            yield self.spawnState()
            yield self.idleState(750)


    def idleState(self, time=50):
        while time > 0:
            time -= 1
            self.anim = 'idle'
            
            # This bit is for gradual destruction frames.
            # DO NOT FUCK WITH IT ANDY.
            self.direction = int(int(self.stats.hp - 1) / int(self.divisor))
            
            yield None
        return

    def spawnState(self):

        if self.jellyCount < self.MAX_JELLIES:
            
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
                
                while len(ika.EntitiesAt(p[0], p[1], tw, th, self.ent.layer)) > 1:
                    num = ika.Random(0, len(positions))
                    p = positions[num]
                    yield None
        
                jelly_ent = ika.Entity(p[0], p[1], self.ent.layer, "jelly.ika-sprite")
        
                engine.addEntity(createJelly(jelly_ent, self))
                self.jellyCount += 1
        
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
            sound.enemyHit.Play()
