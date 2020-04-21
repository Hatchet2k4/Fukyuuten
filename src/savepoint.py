import dir
import engine
import saveloadmenu
import effects
import animator
from entity import Entity

class SavePoint(Entity):

    SPRITE = 'savepoint.ika-sprite'

    __anim = {
        'bounce' : ((
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
            animator.makeAnim(range(4), 10),
        ), True),
    }

    def __init__(self, ent):
        super(SavePoint, self).__init__(ent, self.__anim)
        self.direction = dir.DOWN
        self.isTouching = False
        self.interruptable = False
        self.invincible = True
        self.anim = 'bounce'

    def update(self):
        self.animate()

        t = self.touches(engine.player)
        if t and not self.isTouching:
            # bump the player backward, so he's not touching us anymore.
            effects.fadeOut(50, draw=engine.raw_draw)
            engine.player.stats.hp = 999
            engine.player.stats.mp = 999
            dx, dy = dir.delta[dir.invert[engine.player.direction]]
            engine.player.x += dx * 3
            engine.player.y += dy * 3
            # TODO: neato fadeout, etc.
            # "Do you wish to save?" "Yes/No"
            self.isTouching = True
            engine.raw_draw()
            saveloadmenu.saveMenu()
            effects.fadeIn(50, draw=engine.raw_draw)
            engine.synchTime()
        elif not t:
            self.isTouching = False
