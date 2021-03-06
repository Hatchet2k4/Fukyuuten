
import ika
import engine
import sound
import controls
import dir

from entity import Entity
from enemy import Enemy
from goblin import Arrow

thrustRange = ((-22,  -2, 16,  8),
    ( 15,  -2, 16,  8),
    (  6, -27, 10, 27),
    (  6,  17, 10, 12),
    (-22,  -2, 16,  8),
    ( 15,  -2, 16,  8),
    (-22,  -2, 16,  8),
    ( 15,  -2, 16,  8)
)


slashRange = (
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8),
     (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8),
     ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-14, -12, 10, 22), ( -4, -22, 10, 22), (  6, -22, 10, 22),
     ( 16, -12, 10, 22), ( 16, -22, 10, 22)),
    (( 16,  17, 10, 12), ( 16,  17, 10, 12), (  6,  17, 10, 12),
     ( -4,  17, 10, 12), (-14,  17, 10, 12)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8),
     (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8),
     ( 15,   4, 14,  8), ( 15,  10, 12,  8)),
    ((-18, -14, 12,  8), (-20,  -8, 14,  8), (-22,  -2, 16,  8),
     (-20,   4, 14,  8), (-18,  10, 12,  8)),
    (( 15, -14, 12,  8), ( 15,  -8, 14,  8), ( 15,  -2, 16,  8),
     ( 15,   4, 14,  8), ( 15,  10, 12,  8))
)


backSlashRange = [x[::-1] for x in slashRange]


class Sword(object):
    SPRITE = 'sword.ika-sprite'
    ICON = 'icon_sword.png'

    def __init__(self, item=None):
        self.item = item
        
    def attack1(self, me):
        self.me = me
        return self.slashState(me)

    def attack2(self, me):
        return self.thrustState(me)

    def drawRect(self, ent, x, y, frame):
        d = self.me.direction
        i = self.me._animator.index

        ent.Draw(x, y, frame)

        x += ent.hotx
        y += ent.hoty

        rx, ry, w, h = slashRange[d][i]

        ika.Video.DrawRect(x + rx, y + ry, x + rx + w, y + ry + h, ika.RGB(255, 255, 255))


    def slashState(self, me):
        if 0: me.overlay.renderscript = self.drawRect

        me.stop()
        me.anim = 'slash'
        r = slashRange[me.direction]
        thrust = False
        backslash = False
        backthrust = False
        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = set([])
        sound.sword1.Play()
        while not me._animator.kill:
            rect = list(r[me._animator.index]) + [me.layer]
            rect[0] += me.x
            rect[1] += me.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                if e is me.overlay or e in hitList: continue

                x = engine.entFromEnt[e]

                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.add(x)
                    x.hurt(me.stats.att, 120, me.direction)
                    me.giveMPforHit()

                elif isinstance(x, Arrow):
                    hitList.add(x)
                    sound.deflect.Play()
                    engine.destroyEntity(x)

            if controls.up() and me.direction == dir.DOWN:
                backthrust = True
            elif controls.down() and me.direction == dir.UP:
                backthrust = True
            elif controls.left() and me.direction in [dir.RIGHT, dir.UPRIGHT, dir.DOWNRIGHT]:
                backthrust = True
            elif controls.right() and me.direction in [dir.LEFT, dir.UPLEFT, dir.DOWNLEFT]:
                backthrust = True
            elif controls.attack1() and not thrust:
                backslash = True
            elif controls.attack2() and not backslash:
                thrust = True
            yield None

        if 0: me.overlay.renderscript = None

        if thrust:
            me.state = self.thrustState(me)
        elif backslash:
            me.state = self.backSlashState(me)
        else:
            # Stall:
            count = 10
            while count > 0:
                count -= 1
                #if controls.attack2():
                #    me.state = me.thrustState()
                yield None

        yield None

    def backSlashState(self, me):
        me.stop()
        me.anim = 'backslash'
        r = backSlashRange[me.direction]
        # when we hit an entity, we append it here so that
        # we know not to hurt it again.
        hitList = []
        sound.sword2.Play()
        while not me._animator.kill:
            rect = list(r[me._animator.index]) + [me.layer]
            rect[0] += me.x
            rect[1] += me.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                if e is me.overlay: continue

                x = engine.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                    hitList.append(x)
                    x.hurt(me.stats.att, 140, me.direction)
                    me.giveMPforHit()

            yield None

        # Stall:
        count = 20
        while count > 0:
            count -= 1
            yield None

    def thrustState(self, me):
        if me.direction == dir.UPLEFT or me.direction == dir.DOWNLEFT:
            me.direction = dir.LEFT
        elif me.direction == dir.UPRIGHT or me.direction == dir.DOWNRIGHT:
            me.direction = dir.RIGHT

        class SpeedSaver(object):
            def __init__(_self):
                _self.s = me.speed
            def __del__(_self):
                me.speed = _self.s

        ss = SpeedSaver()
        me.anim = 'thrust'
        me.speed += 200
        me.move(me.direction, 1000)
        r = thrustRange[me.direction] + (me.layer,)
        rect = list(r)
        sound.sword3.Play()

        hitlist = set()

        def hurt():
            rect[0] = r[0] + me.x
            rect[1] = r[1] + me.y
            ents = ika.EntitiesAt(*rect)
            for e in ents:
                if e in hitlist: continue

                hitlist.add(e)

                x = engine.entFromEnt[e]
                if isinstance(x, Enemy) and not x.invincible:
                    x.hurt(int(me.stats.att * 1.5), 150, me.direction)
                    me.giveMPforHit()
                    #me.stop()
                    return False

            return False

        i = 8
        while i > 0:
            i -= 1
            me.speed -= (8 - i) * 5

            result = hurt()
            if result: break

            yield None

        spin = None
        i = 50
        while i > 0:
            i -= 1

            if controls.attack1() and spin is None:
                # tiny window: press the slash button just as the thrust finishes to do uber-attack!
                if i > 40: spin = False
                else: spin = True

            me.speed = max(10, me.speed - 10)
            yield None
        me.stop()

        if spin:
            print 'Spin!!! NYI omfg'

