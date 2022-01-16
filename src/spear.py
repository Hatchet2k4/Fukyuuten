
import ika
import engine
import sound
import controls
import dir

from entity import Entity
from enemy import Enemy

from obstacle import Obstacle
from quake import Quake


lungeRange = (
    (-25,   0, 26, 16),
    ( 16,   0, 26, 16),
    (  0, -30, 16, 26),
    (  0,  16, 16, 26),
    (-25,   0, 26, 16),
    ( 16,   0, 26, 16),
    (-25,   0, 26, 16),
    ( 16,   0, 26, 16),
)


class Spear(object):
    SPRITE = 'spear.ika-sprite'
    ICON = 'icon_spear.png'

    def __init__(self, item=None):
        self.item = item
        
    def attack1(self, me):
        return self.lungeState(me)

    def attack2(self, me):
        return self.chargeState(me)

    def lungeState(self, me):
        class Sentinel(object):
            def __init__(_self):
                _self.speed = me.speed
            def __del__(_self):
                me.speed = _self.speed
        s = Sentinel()

        sound.spear1.Play()
        
        me.anim = 'lunge'
        me.speed += 200
        me.direction = dir.straighten[me.direction]
        me.move(me.direction, 32)
        yield None

        hitlist = set()

        # do .... while me.isMoving()
        while True:
            # TODO: hit detection here.  Everything on the hitlist
            # should stay a constant distance from the player, and
            # only suffer recoil when the lunge is through.

            ents = me.detectCollision(lungeRange[me.direction])
            for e in ents:
                if e in hitlist: continue
                hitlist.add(e)

                if isinstance(e, Enemy):
                    e.hurt(int(me.stats.att * 1.5), 190, me.direction)

            yield None

            if not me.isMoving():
                break

        i = 60
        while i > 0:
            i -= 1
            yield None

    def chargeState(self, me):
        me.anim = 'charge'
        me.stop()

        sound.spear2.Play()
        
        power = 1.5
        animcount = 0
        while controls.attack2.position:
            power = min(4, power + 0.01)

            # speed up the animation
            animcount += 25 * power
            while animcount > 100:
                me.animate()
                animcount -= 100

            if controls.attack1():
                if power > 2.0:
                    
                    me.state = self.powerLungeState(me, power)
                else:
                    me.state = self.lungeState(me)

            yield None

    def powerLungeState(self, me, power):
        class Saver(object):
            def __init__(_self):
                _self.speed = me.speed
                _self.o = me.ent.entobs
                _self.i = me.invincible
                _self.l = engine.camera.locked
            def __del__(_self):
                me.speed = _self.speed
                me.ent.entobs = _self.o
                me.invincible = _self.i
                engine.camera.locked = _self.l
        saver = Saver()

        sound.spear3.Play()
        
        me.direction = dir.straighten[me.direction]

        me.stop()
        me.anim = 'charge'

        camera = engine.camera
        camera.locked = True
        dx, dy = dir.delta[me.direction]

        #sound.crushingGale.Play()

        me.anim = 'lunge'

        r = lungeRange[me.direction] + (me.layer,)
        me.move(me.direction, int(16 + power * 2))
        me.speed *= 5

        while me._animator.index == 0:
            yield None

        hitlist = set()
        while not me._animator.kill:
            ents = me.detectCollision(r)
            for e in ents:
                if e in hitlist: continue
                hitlist.add(e)

                if isinstance(e, Enemy) and not e.invincible:
                    e.hurt(
                        int(me.stats.att * power),
                        200 * power,
                        me.direction
                    )

                    engine.mapThings.append(Quake(10))

            yield None

        me.stop()
        # stall
        for i in range(20):
            yield None
