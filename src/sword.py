
import ika
import engine
import sound
import controls
import dir

from entity import Entity
from enemy import Enemy
from goblin import Arrow
import powerup
from powerup import _Powerup


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

def tilesAt(x, y, w, h, l):
    poslist = [ [x/16, y/16], [(x+w)/16, y/16], [x/16, (y+h)/16], [(x+w)/16, (y+h)/16] ]
    resultlist= []
    for p in poslist:
        resultlist.append( p + [ika.Map.GetTile(p[0], p[1], l)] )
    resultlist = dedupe(resultlist)
        
    return resultlist

def dedupe(lst):
    new_list = []
    for a in lst:
        if a not in new_list:
            new_list.append(a)
    return new_list

class Leaf(Entity):
    SPRITE = 'flowerleaf.ika-sprite'

    ANIM = {
        'fall' : ((
            ((0, 1000),), 
            ((1, 1000),),
            ((0, 1000),),
            ((1, 1000),),
            ((0, 1000),),
            ((1, 1000),),
            ((0, 1000),),
            ((1, 1000),),
        ), True),
    }

    def __init__(self, ent):
        super(Leaf, self).__init__(ent, self.ANIM)

        self.directions = [dir.DOWNLEFT, dir.DOWNRIGHT]
        self.direction =  self.directions[ika.Random(0, 2)]

        self.invincible = True
        self.speed = 20        
        self.ent.isobs = False
        self.ent.entobs = False
        self.ent.mapobs = False
        self.count=0
        self.framecount=0

    def defaultState(self):
        self.move(self.direction, 5)
        self.anim = 'fall'

        while True:
            if self.count<50:                        
                self.count+=1
                self.framecount+=1
                if self.framecount>8 and ika.Random(0, 6)==0:
                    self.framecount=0
                    if self.direction == dir.DOWNLEFT: self.direction=dir.DOWNRIGHT
                    else: self.direction = dir.DOWNLEFT
                self.move(self.direction, 5)                
                yield None
            else:
                engine.destroyEntity(self)
                yield None

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

    def cutBush(self, me, rect):
        tiles = tilesAt(*rect)
        #ika.Log(str(tiles))
        for t in tiles:
            if t[2] in [78, 368, 369, 370]: #bush!
                ika.Map.SetTile(t[0], t[1], me.layer, 0)
                ika.Map.SetObs(t[0], t[1], me.layer, 0)
                flower = Leaf(ika.Entity(t[0]*16+2, t[1]*16+4, me.layer, 'flowercenter.ika-sprite'))
                engine.addEntity(flower)                      
                for i in range(5 + ika.Random(0, 3)):
                    lx=t[0]*16+ika.Random(-4, 12)
                    ly=t[1]*16+ika.Random(0, 7)                        
                    leaf = Leaf(ika.Entity(lx, ly, me.layer, 'flowerleaf.ika-sprite'))                        
                    engine.addEntity(leaf)
                chance = ika.Random(0,100)
                if chance > 90: 
                    shell = powerup.createShell(ika.Entity(t[0]*16+4, t[1]*16+4, me.layer, 'seashell.ika-sprite'))
                    engine.addEntity(shell)
                elif chance > 80: 
                    berry = powerup.createRedBerry(ika.Entity(t[0]*16+4, t[1]*16+4, me.layer, 'berry.ika-sprite'))
                    engine.addEntity(berry)
                    
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
                if e in engine.entFromEnt:
                    x = engine.entFromEnt[e]

                    if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                        hitList.add(x)
                        x.hurt(int(me.stats.att), 120, me.direction)
                        me.giveMPforHit()

                    elif isinstance(x, Arrow):
                        hitList.add(x)
                        sound.deflect.Play()
                        engine.destroyEntity(x)
                        
                    elif isinstance(x, _Powerup):
                        x.touch()

            self.cutBush(me, rect)
            
                      
                        
            if (controls.up() or controls.joy_up())  and me.direction == dir.DOWN:
                backthrust = True
            elif (controls.down() or controls.joy_down()) and me.direction == dir.UP:
                backthrust = True
            elif (controls.left() or controls.joy_left()) and me.direction in [dir.RIGHT, dir.UPRIGHT, dir.DOWNRIGHT]:
                backthrust = True
            elif (controls.right() or controls.joy_right()) and me.direction in [dir.LEFT, dir.UPLEFT, dir.DOWNLEFT]:
                backthrust = True
            elif (controls.attack1() or controls.joy_attack1()) and not thrust:
                backslash = True
            elif (controls.attack2() or controls.joy_attack2())  and not backslash:
                thrust = True
            yield None

        if 0: me.overlay.renderscript = None

        if thrust:
            me.state = self.thrustState(me)
        elif backslash:
            me.state = self.backSlashState(me)
        else:
            # Stall:
            count = 8
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
                if e in engine.entFromEnt:
                    x = engine.entFromEnt[e]
                    if isinstance(x, Enemy) and not x.invincible and x not in hitList:
                        hitList.append(x)
                        x.hurt(int(me.stats.att), 140, me.direction)
                        me.giveMPforHit()
                    elif isinstance(e, _Powerup):
                        e.touch()                    
            self.cutBush(me, rect)
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
                elif isinstance(e, _Powerup):
                    e.touch()
                    
            return False

        i = 8
        while i > 0:
            i -= 1
            me.speed -= (8 - i) * 5
            self.cutBush(me, rect)
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


