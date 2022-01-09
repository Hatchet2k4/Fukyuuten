
import ika
import engine
import sound
import dir
from entity import Entity

class _GrappleEntity(Entity):
    '''Specifically the entity that is used to display the grapple hook'''
    SPRITE = 'rope.ika-sprite'
    ICON = 'icon_grapple.png'
    IMAGE = 'gfx/rope.png'

    ANIM = {
        'fly': ((
            ((0, 1),),
            ((1, 1),),
            ((2, 1),),
            ((3, 1),),
            ((0, 1),),
            ((1, 1),),
            ((0, 1),),
            ((1, 1),),
        ), False),
    }

    def __init__(self, x, y, layer, direction):
        super(_GrappleEntity, self).__init__(ika.Entity(x, y, layer, self.SPRITE), self.ANIM)

        self.ent.entobs = False
        self.ent.isobs = False

        self.ent.renderscript = self.__render

        self.direction = direction
        self.image = ika.Image(self.IMAGE)
        self.speed = 250

    def __render(self, entity, x, y, frame):
        ox = x
        oy = y

        y += self.ent.hoty

        xw = self.x - x
        yw = self.y - y

        p = engine.player
        px, py = p.x - xw, p.y - yw

        # Good god what have I unleashed. @_@
        # most of the idiotic little +=s and -=s are just to make graphics line up.

        if self.direction in (dir.UP, dir.DOWN):
            w = self.image.width
            y2 = py

            if self.direction == dir.DOWN:
                y -= 2
                y2 += 7
            else:
                y += 3

            ika.Video.DistortBlit(
                self.image,
                (x + w, y),
                (x + w, y2),
                (x, y2),
                (x, y)
            )

        else:
            y -= 5
            w = px

            if self.direction == dir.RIGHT:
                w += 20
            else:
                x += self.image.width
                #w -= 4

            w -= x

            ika.Video.ScaleBlit(self.image, x, y, w, self.image.height)

        entity.Draw(ox, oy, frame)

    def defaultState(self):
        self.anim = 'fly'
        self.move(self.direction, 144)

        while True:
            oldx = self.x
            oldy = self.y

            yield None

            if self.x == oldx and self.y == oldy:
                self.stop()

class Grapple(object):
    GRIPPABLE_TILES = {
        'level1.vsp' : set((126, 280, 281, 282, 283, 284)),
        'green.vsp' : set((363,79)),
    }

    def activate(self, me):
        return self.grappleState(me)

    def grappleState(self, me):
        sound.grapple1.Play()
        direction = dir.straighten[me.direction]
        x = me.x
        y = me.y

        # HACK: work around rectangular hotspot junk.
        dx, dy = dir.delta[direction]
        if dx > 0: x += 16
        if dy > 0: y += 16

        if me.direction in (dir.UP, dir.DOWN):
            x += 7
        if me.direction in (dir.LEFT, dir.RIGHT):
            y += 2

        me.anim = 'grapplethrow'
        me.invincible = True

        grapple = _GrappleEntity(x, y, me.layer, direction)
        engine.addEntity(grapple)
        yield None # needed to give the grapple a moment to start moving

        while grapple.isMoving():
            yield None

        dx, dy = dir.delta[grapple.direction]
        tx = grapple.x / ika.Tileset.width + dx
        ty = grapple.y / ika.Tileset.height + dy
        tile = ika.Map.GetTile(tx, ty, grapple.layer)

        grippableTiles = self.GRIPPABLE_TILES.get(ika.Map.tilesetname, ())

        if tile in grippableTiles:
            me.state = self.pullState(me, grapple)
        else:
            me.invincible = False
            me.state = me.defaultState()
            engine.destroyEntity(grapple)

        yield None

    def pullState(self, me, grapple):
        sound.grapple2.Play()
        me.anim = 'grapplepull'

        if me.direction in (dir.UP, dir.DOWN):
            dist = abs(grapple.y - engine.player.y)
        else:
            dist = abs(grapple.x - engine.player.x)

        if me.direction in (dir.RIGHT, dir.DOWN):
            dist -= 15

        class Sentinel(object):
            def __init__(_self):
                _self.speed = me.speed

            def __del__(_self):
                me.speed = _self.speed
                me.invincible = False
                me.mapobs = True
                me.entobs = True

                engine.destroyEntity(grapple)

        s = Sentinel()

        oldSpeed = me.speed
        me.invincible = True
        me.ent.mapobs = False
        me.ent.entobs = False

        me.move(me.direction, dist)

        yield None

        factor = 3

        me.speed = 0

        while me.ent.IsMoving():
            me.speed += factor
            me.speed = min(grapple.speed, me.speed)
            yield None

        me.ent.mapobs = True
        me.ent.entobs = True
        me.speed = oldSpeed

