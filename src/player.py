import ika
import animator
import controls
import dir
import engine
import sound
import item
from caption import Caption
from enemy import Enemy
from goblin import Arrow
from entity import Entity
from gameover import GameOverException
from statset import StatSet

from sword import Sword
from spear import Spear
from grapple import Grapple


PLAYER_SPRITE = 'anastasia.ika-sprite'

# Helper functions.  More for clarity than anything else.
def _frame(index, delay, weaponIndex=3, weaponPos=(0,0)):
    return (index, delay, weaponIndex, weaponPos)

def _strand(*args):
    return args

def _makeAnim(frames, delay):
    return tuple(_frame(frame, delay) for frame in frames)

# one entry for each direction
_playerAnim = {
    'stand': ((
            _strand(_frame(2, 1000)),
            _strand(_frame(3, 1000)),
            _strand(_frame(1, 1000)),
            _strand(_frame(0, 1000)),
            _strand(_frame(2, 1000)),
            _strand(_frame(3, 1000)),
            _strand(_frame(2, 1000)),
            _strand(_frame(3, 1000)),
        ), True),
    'walk': ((
        _makeAnim(range(12, 16), 12),
        _makeAnim(range(16, 20), 12),
        _makeAnim(range( 8, 12), 12),
        _makeAnim(range( 4,  8), 12),
        _makeAnim(range(12, 16), 12),
        _makeAnim(range(16, 20), 12),
        _makeAnim(range(12, 16), 12),
        _makeAnim(range(16, 20), 12)), True),
    'slash': (( #+4 hackery because I added 4 frames to sword overlay
        _strand(_frame(44,  8,  8+4), _frame(45, 6,  9+4), _frame(46, 5, 10+4), _frame(47, 6, 11+4)),
        _strand(_frame(48,  8, 12+4), _frame(49, 6, 13+4), _frame(50, 5, 14+4), _frame(51, 6, 15+4)),
        _strand(_frame(40,  8,  4+4), _frame(41, 6,  5+4), _frame(42, 5,  6+4), _frame(43, 6,  7+4)),
        _strand(_frame(36,  8,  0+4), _frame(37, 6,  1+4), _frame(38, 5,  2+4), _frame(39, 6,  3+4)),
        _strand(_frame(44,  8,  8+4), _frame(45, 6,  9+4), _frame(46, 5, 10+4), _frame(47, 6, 11+4)),
        _strand(_frame(48,  8, 12+4), _frame(49, 6, 13+4), _frame(50, 5, 14+4), _frame(51, 6, 15+4)),
        _strand(_frame(44,  8,  8+4), _frame(45, 6,  9+4), _frame(46, 5, 10+4), _frame(47, 6, 11+4)),
        _strand(_frame(48,  8, 12+4), _frame(49, 6, 13+4), _frame(50, 5, 14+4), _frame(51, 6, 15+4)),
        ), False),
    'backslash': ((
        _strand(_frame(47,  8, 11+4), _frame(46, 6, 10+4), _frame(45, 5,  9+4), _frame(44, 6,  8+4)),
        _strand(_frame(51,  8, 15+4), _frame(50, 6, 14+4), _frame(49, 5, 13+4), _frame(48, 6, 12+4)),
        _strand(_frame(43,  8,  7+4), _frame(42, 6,  6+4), _frame(41, 5,  5+4), _frame(40, 6,  4+4)),
        _strand(_frame(39,  8,  3+4), _frame(38, 6,  2+4), _frame(37, 5,  1+4), _frame(36, 6,  0+4)),
        _strand(_frame(47,  8, 11+4), _frame(46, 6, 10+4), _frame(45, 5,  9+4), _frame(44, 6,  8+4)),
        _strand(_frame(51,  8, 15+4), _frame(50, 6, 14+4), _frame(49, 5, 13+4), _frame(48, 6, 12+4)),
        _strand(_frame(47,  8, 11+4), _frame(46, 6, 10+4), _frame(45, 5,  9+4), _frame(44, 6,  8+4)),
        _strand(_frame(51,  8, 15+4), _frame(50, 6, 14+4), _frame(49, 5, 13+4), _frame(48, 6, 12+4)),
        ), False),
    'thrust' : ((
        _strand(_frame(28, 10, 24+4), _frame(29, 10, 25+4), _frame(30, 10, 26+4)),
        _strand(_frame(32, 10, 28+4), _frame(33, 10, 29+4), _frame(34, 10, 30+4)),
        _strand(_frame(24, 10, 20+4), _frame(25, 10, 21+4), _frame(26, 10, 22+4)),
        _strand(_frame(20, 10, 16+4), _frame(21, 10, 17+4), _frame(22, 10, 18+4)),
        _strand(_frame(28, 10, 24+4), _frame(29, 10, 25+4), _frame(30, 10, 26+4)),
        _strand(_frame(32, 10, 28+4), _frame(33, 10, 29+4), _frame(34, 10, 30+4)),
        _strand(_frame(28, 10, 24+4), _frame(29, 10, 25+4), _frame(30, 10, 26+4)),
        _strand(_frame(32, 10, 28+4), _frame(33, 10, 29+4), _frame(34, 10, 30+4)),
        ), False),
    'lunge' : ((
        _strand(_frame(28, 10,  8), _frame(29, 10,  9), _frame(30, 10, 10)),
        _strand(_frame(32, 10, 12), _frame(33, 10, 13), _frame(34, 10, 14)),
        _strand(_frame(24, 10,  4), _frame(25, 10,  5), _frame(26, 10,  6)),
        _strand(_frame(20, 10,  0), _frame(21, 10,  1), _frame(22, 10,  2)),
        _strand(_frame(28, 10,  8), _frame(29, 10,  9), _frame(30, 10, 10)),
        _strand(_frame(32, 10, 11), _frame(33, 10, 12), _frame(34, 10, 13)),
        _strand(_frame(28, 10,  8), _frame(29, 10,  9), _frame(30, 10, 10)),
        _strand(_frame(32, 10, 11), _frame(33, 10, 12), _frame(34, 10, 13)),
        ), False),
    'charge' : ((
        _strand(_frame(55, 10, 16, (-7, -7)), _frame(55, 10, 17, (-7, -7)), _frame(55, 10, 18, (-7, -7)), _frame(55, 10, 19, (-7, -7))),
        _strand(_frame(53, 10, 20, ( 7, -7)), _frame(53, 10, 21, ( 7, -7)), _frame(53, 10, 22, ( 7, -7)), _frame(53, 10, 23, ( 7, -7))),
        _strand(_frame(54, 10, 24, (11,  1)), _frame(54, 10, 25, (11,  1)), _frame(54, 10, 26, (11,  1)), _frame(54, 10, 27, (11,  1))),
        _strand(_frame(52, 10, 27, (-11, 5)), _frame(52, 10, 26, (-11, 5)), _frame(52, 10, 25, (-11, 5)), _frame(52, 10, 24, (-11, 5))),
        _strand(_frame(55, 10, 16, (-7, -7)), _frame(55, 10, 17, (-7, -7)), _frame(55, 10, 18, (-7, -7)), _frame(55, 10, 19, (-7, -7))),
        _strand(_frame(53, 10, 21, (-7, -7)), _frame(53, 10, 22, (-7, -7)), _frame(53, 10, 23, (-7, -7)), _frame(53, 10, 24, (-7, -7))),
        _strand(_frame(55, 10, 16, (-7, -7)), _frame(55, 10, 17, (-7, -7)), _frame(55, 10, 18, (-7, -7)), _frame(55, 10, 19, (-7, -7))),
        _strand(_frame(53, 10, 21, (-7, -7)), _frame(53, 10, 22, (-7, -7)), _frame(53, 10, 23, (-7, -7)), _frame(53, 10, 24, (-7, -7))),
        ), True),
    'grapplethrow' : ((
        _strand(_frame(64, 1000)),
        _strand(_frame(66, 1000)),
        _strand(_frame(62, 1000)),
        _strand(_frame(60, 1000)),
        _strand(_frame(64, 1000)),
        _strand(_frame(66, 1000)),
        _strand(_frame(64, 1000)),
        _strand(_frame(66, 1000)),
        ), False),
    'grapplepull' : ((
        _strand(_frame(65, 1000)),
        _strand(_frame(67, 1000)),
        _strand(_frame(63, 1000)),
        _strand(_frame(61, 1000)),
        _strand(_frame(65, 1000)),
        _strand(_frame(67, 1000)),
        _strand(_frame(65, 1000)),
        _strand(_frame(67, 1000)),
        ), False),
    'hurt' : ((
        _strand(_frame(35, 1000)),
        _strand(_frame(31, 1000)),
        _strand(_frame(23, 1000)),
        _strand(_frame(27, 1000)),
        _strand(_frame(35, 1000)),
        _strand(_frame(31, 1000)),
        _strand(_frame(35, 1000)),
        _strand(_frame(31, 1000)),
        ), False),
    #~ 'die': ((
        #~ zip((90,  91,  92), (20, 20, 1000)),
        #~ zip((99, 100, 101), (20, 20, 1000)),
        #~ zip((72,  73,  74), (20, 20, 1000)),
        #~ zip((81,  82,  83), (20, 20, 1000)),
        #~ zip((90,  91,  92), (20, 20, 1000)),
        #~ zip((99, 100, 101), (20, 20, 1000)),
        #~ zip((90,  91,  92), (20, 20, 1000)),
        #~ zip((99, 100, 101), (20, 20, 1000))), False),
    #~ # temporary:  copy the normal standing frames.
    #~ 'magic': ((
        #~ ((27, 1000),),
        #~ ((18, 1000),),
        #~ (( 9, 1000),),
        #~ (( 0, 1000),),
        #~ ((27, 1000),),
        #~ ((18, 1000),),
        #~ ((27, 1000),),
        #~ ((18, 1000),)), True),
    #~ 'shiver': ((zip((65, 47, 56, 38), (5, 5, 5, 5)),
        #~ zip((56, 38, 65, 47), (5, 5, 5, 5)),
        #~ zip((47, 56, 38, 65), (5, 5, 5, 5)),
        #~ zip((38, 65, 47, 56), (5, 5, 5, 5)),
        #~ zip((65, 47, 56, 38), (5, 5, 5, 5)),
        #~ zip((56, 38, 65, 47), (5, 5, 5, 5)),
        #~ zip((65, 47, 56, 38), (5, 5, 5, 5)),
        #~ zip((56, 38, 65, 47), (5, 5, 5, 5))), True),
}


initialStats = StatSet(
    maxhp=120,
    hp=120,
    maxmp=15,
    mp=15,
    att=10,
    mag=5,
    pres=5,
    mres=3,
    level=1,
    exp=0,
)

class _Anim(animator.Animator):
    def __init__(self, *args, **kw):
        self.index = 0
        self.weaponIndex = 0
        self.weaponPos = (0, 0)
        super(_Anim, self).__init__(*args, **kw)

    def getCurFrame(self):
        return self.__dict__['curFrame']

    def setCurFrame(self, value):
        # EVIL
        self.__dict__['curFrame'] = value
        if self.anim is not None:
            self.weaponIndex = self.anim[self.index][2]
            self.weaponPos = self.anim[self.index][3]

    curFrame = property(getCurFrame, setCurFrame)


class Player(Entity):

    def __init__(self, x=0, y=0, layer=0):
        super(Player, self).__init__(
            ika.Entity(x, y, layer, PLAYER_SPRITE),
            _playerAnim
        )

        self._animator = _Anim()

        self.state = self.standState()
        self.stats = initialStats.clone()
        
        self.baseStats = self.stats.clone()

        self.expFactor = 50.0
        self.exponent = 1.9

        self.sword = Sword()
        self.spear = Spear()
        self.spear.item = item.Item('Fishing Pole')
        self.sword.item = item.Item('Sharp Slicer')
        self.armor = None
        
        self.grapple = Grapple()
        
        self.items = []
        
        #self.weapon = self.spear
        self.weapon = self.sword
        
        #print `self.weapon.item.overlaySprite`

    def giveXP(self, amount):
        self.stats.exp += amount * (100 / self.expFactor) / (self.exponent ** (self.stats.level - 1))
        if self.stats.exp >= 100:
            self.levelUp()

    def update(self):
        try:
            super(Player, self).update()
        finally:
            self.overlay.specframe = self._animator.weaponIndex
            x, y = self._animator.weaponPos
            self.overlay.x = self.x + x
            self.overlay.y = self.y + y
            self.overlay.layer = self.layer

    def setLayer(self, lay):
        super(Player, self).setLayer(lay)
        self.overlay.layer = lay
    layer = property(Entity.getLayer, setLayer)

    def levelUp(self):
        #sound.achievement.Play()

        while self.stats.exp >= 100:
            self.stats.maxhp += ika.Random(14, 20)
            self.stats.maxmp += ika.Random(2, 5)

            statlist = []
            for n in range(8 + self.stats.level/3):
                if not statlist:
                    statlist = ['att', 'mag', 'pres', 'mres']
                s = statlist[ika.Random(0,len(statlist))]

                setattr(self.stats, s,
                    getattr(self.stats, s) + 1
                )

                statlist.remove(s)

            self.stats.level += 1
            self.stats.exp -= 100
            self.stats.exp = self.stats.exp * (self.exponent ** (self.stats.level - 2)) / (self.exponent ** (self.stats.level - 1))

        engine.things.append(Caption('Level %i!' % self.stats.level))

    def calcSpells(self):
        '''Figures out what spells the player has access to, based on
           the flags set in the saveData dictionary.
        '''
        pass

    def defaultState(self):
        return self.standState()

    def standState(self):
        self.stop()
        self.anim = 'stand'
        while True:
            if controls.attack1() or controls.joy_attack1():
                self.state = self.weapon.attack1(self)

            elif controls.attack2() or controls.joy_attack2():
                self.state = self.weapon.attack2(self)

            elif (controls.tool1() or controls.joy_tool1()) and 'grapple' in engine.saveData:
                self.state = self.grapple.activate(self)

            elif (controls.left() or controls.right() or
                 controls.up() or controls.down() or
                 controls.joy_left() or controls.joy_right() or
                 controls.joy_up() or controls.joy_down()
            ):
                self.state = self.walkState()

            #elif (controls.left() or controls.right() or
            #     controls.up() or controls.down()
            #):
            #    self.state = self.walkState()
            #    self._state()  # get the walk state started right now.

            if not self.stats.mp:
                self.invincible = False
                self.ent.visible = 1
                self.speed = 100
            yield None

    def walkState(self):
        oldDir = self.direction
        self.anim = 'walk'
        while True:
            if controls.attack1() or controls.joy_attack1():
                self.state = self.weapon.attack1(self)
                yield None

            elif controls.attack2() or controls.joy_attack2():
                self.state = self.weapon.attack2(self)
                yield None

            elif controls.left() or controls.joy_left():
                if controls.up() or controls.joy_up():
                    d = dir.UPLEFT
                elif controls.down() or controls.joy_down():
                    d = dir.DOWNLEFT
                else:
                    d = dir.LEFT
            elif controls.right() or controls.joy_right():
                if controls.up() or controls.joy_up():
                    d = dir.UPRIGHT
                elif controls.down() or controls.joy_down():
                    d = dir.DOWNRIGHT
                else:
                    d = dir.RIGHT
            elif controls.up() or controls.joy_up():
                d = dir.UP
            elif controls.down() or controls.joy_down():
                d = dir.DOWN
            else:
                self.state = self.standState()
                yield None

            self.move(d)
            # handle animation and junk
            if d != oldDir:
                self.anim = 'walk'
                self.direction = d
                oldDir = d
            yield None

    def die(self):
        self.state = self.deathState()
        self._state()
        #self.anim = 'die'
        raise GameOverException()


    def deathState(self):
        self.invincible = True
        sound.playerDie.Play()
        s = self.hurtState(300, dir.invert[self.direction])
        yield s.next()
        #self.anim = 'die'
        for x in s:
            yield None
        while True:
            yield None

    def giveMPforHit(self):
        self.stats.mp += ika.Random(0, min(4, 2 + self.stats.level / 10))

    def setWeapon(self, weapon):
        self.__weapon = weapon

    weapon = property(lambda self: self.__weapon, setWeapon)
    overlay = property(lambda self: self.weapon.item.overlay)
