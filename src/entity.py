import ika
import dir
import engine
import sound
from animator import Animator
from statset import StatSet
import gui
from caption import DamageCaption

def _temp():
    yield None
GeneratorType = type(_temp())
del _temp


class EntityError(Exception):
    pass


class Entity(object):
    '''Most every interactive thing in the game is an Entity.'''

    # arbitrary, and meaningless for the most part.
    DIST = 48


    def __init__(self, ent, anim):
        # ent can be None if all of the entity manipulating methods are
        # overidden.
        self.ent = ent
        self.stats = StatSet()
        self.stats.hp = 1
        self._animator = Animator()
        self._anim = anim
        self.direction = dir.DOWN  # arbitrary
        self.interruptable = True  # if false, no state changes will occur
        self.invincible = False
        self._state = self.defaultState().next

    def destroy(self):
        for k in self.__dict__.keys():
            self.__dict__[k] = None

    def update(self):
        '''Main update routine.
           Override if you must, use the state mechanism if you can.
        '''
        self.animate()
        try:
            return self._state()
        except StopIteration:
            self.state = self.defaultState()
            return self._state()

    def die(self, *args):
        engine.destroyEntity(self)

    # if recoil is nonzero, the enemy is blown backwards in a direction,
    # at some speed.  The default direction is backwards
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
            self.state = self.hurtState(recoilSpeed, recoilDir)
        
        x=self.ent.x + self.ent.hotwidth/2 - engine.font.StringWidth(str(amount))/2
        y=self.ent.y 
        engine.addThing(DamageCaption(str(amount), x, y, 40, 250, 0, 0))            

    def recoil(self, speed, direction=None):
        if self.invincible: return

        self.state = self.recoilState(speed, direction or dir.invert[self.direction])

    def _setState(self, newState):
        '''Sets a new state, if possible.

        newState *must* be iterable.
        '''

        # Uninterruptable state is running.  Ignore state change
        if self._state is not None and not self.interruptable: return

        if 0 and newState is None:
            self._state = None

        else:
            try:
                self._state = newState.next
            except NameError:
                raise EntityError('Entity.state must be a generator, not %r' % newState)

    state = property(fset=_setState)

    def defaultState(self):
        while True:
            yield None

    def hurtState(self, recoilSpeed, recoilDir):
        iter = self.recoilState(recoilSpeed, recoilDir)

        class Restorer(object):
            def __init__(_self): _self.invincible = self.invincible
            def __del__(_self):  self.invincible = _self.invincible
        restorer = Restorer()

        self.invincible = True

        count = 30
        for dummy in self.recoilState(recoilSpeed, recoilDir):
            yield None
            count -= 1
            if count == 0:
                self.invincible = restorer.invincible

    def recoilState(self, recoilSpeed, recoilDir):
        class Restorer(object):
            def __init__(_self): _self.s = self.speed
            def __del__(_self): self.speed = _self.s
        rest = Restorer()

        dx, dy = dir.delta[recoilDir]
        self.speed = recoilSpeed
        self.move(recoilDir, 1000000)  # just go until I say stop
        self.anim = 'hurt'
        t = 64

        if self is engine.player:
            sound.playerHit.Play()

        while True:
            t -= 1
            #if t <= 34: self.invincible = rest.i
            self.speed -= t / 8
            yield None
            if t <= 0 or self.speed <= 0: break

        self.direction = dir.invert[self.direction]
        self.ent.Stop()
        yield None

    def detectCollision(self, rect):
        '''Returns a list of entities that are within the rect.
           The rect's position is taken as being relative to the
           entity's position.  This is useful for attacks and such.
        '''
        rect = (
            rect[0] + self.x,
            rect[1] + self.y,
            rect[2],
            rect[3],
            self.layer
        )

        return [
            engine.entFromEnt[e]
            for e in ika.EntitiesAt(*rect)
            if e in engine.entFromEnt
        ]

    def touches(self, ent):
        return self.ent.Touches(ent.ent)

    # Entity methods.
    # Most everything that involves an ika entity should be done here.

    def up(self):
        self.ent.MoveTo(self.ent.x, self.ent.y - self.DIST)
        self.direction = dir.UP

    def down(self):
        self.ent.MoveTo(self.ent.x, self.ent.y + self.DIST)
        self.direction = dir.DOWN

    def left(self):
        self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y)
        self.direction = dir.LEFT

    def right(self):
        self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y)
        self.direction = dir.RIGHT

    def upLeft(self):
        self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y - self.DIST)
        self.direction = dir.UPLEFT

    def upRight(self):
        self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y - self.DIST)
        self.direction = dir.UPRIGHT

    def downLeft(self):
        self.ent.MoveTo(self.ent.x - self.DIST, self.ent.y + self.DIST)
        self.direction = dir.DOWNLEFT

    def downRight(self):
        self.ent.MoveTo(self.ent.x + self.DIST, self.ent.y + self.DIST)
        self.direction = dir.DOWNRIGHT

    def move(self, d, dist = DIST):
        dx, dy = dir.delta[d]
        self.direction = d
        self.ent.MoveTo(
            int(self.ent.x + dist * dx),
            int(self.ent.y + dist * dy)
        )

    def isMoving(self):
        return self.ent.IsMoving()

    def stop(self):
        self.ent.Stop()

    def getX(self):
        return self.ent.x

    def getY(self):
        return self.ent.y

    def setX(self, value):
        self.ent.x = value

    def setY(self, value):
        self.ent.y = value

    def getSpeed(self):
        return self.ent.speed

    def setSpeed(self, value):
        self.ent.speed = value

    def getLayer(self):
        return self.ent.layer

    def setLayer(self, value):
        self.ent.layer = value

    def animate(self):
        self._animator.update(1)
        self.ent.specframe = self._animator.curFrame

    def setAnim(self, value, loop = False):
        a, loop = self._anim[value]
        self._animator.setAnim(a[self.direction], loop)

    x = property(getX, setX)
    y = property(getY, setY)
    moving = property(isMoving)
    speed = property(getSpeed, setSpeed)
    layer = property(getLayer, setLayer)
    anim = property(fset=setAnim)
