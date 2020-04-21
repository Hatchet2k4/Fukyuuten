import engine
import sound
import animator
from entity import Entity

_powerupAnim = {

    'idle': ((
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        animator.makeAnim((0, 1, 2, 1), 10),
        ),
        True
    ),
}

class _Powerup(Entity):

    def __init__(self, ent, *args, **kwargs):
        super(_Powerup, self).__init__(ent, _powerupAnim)
        self.invincible = True
        self.anim = 'idle'
        self.direction = 0
        
        self.args = args
        self.kwargs = kwargs

    def apply(self):
        pass

    def update(self):
        self.animate()
        if self.touches(engine.player):
            engine.destroyEntity(self)
            sound.powerup.Play()
            self.apply()


class RedBerry(_Powerup):
    SPRITE = 'berry.ika-sprite'

    def apply(self):
        engine.player.stats.hp += 10


class GreenBerry(_Powerup):
    SPRITE = 'berry2.ika-sprite'
    
    def apply(self):
        engine.player.stats.hp += 40    


class Seashell(_Powerup):
    SPRITE = 'seashell.ika-sprite'
    
    def apply(self):
        engine.player.stats.money += self.kwargs['money']
        print `engine.player.stats.money`
        

class BlackPearl(_Powerup):
    SPRITE = 'pearl.ika-sprite'
    
    def apply(self):
        engine.player.stats.att += 1
        

class GoldenEgg(_Powerup):
    SPRITE = 'egg.ika-sprite'
    
    def apply(self):
        engine.player.stats.pres += 1
        
        
class Skull(_Powerup):
    SPRITE = 'skull.ika-sprite'
    
    def apply(self):
        pass
        
    
class Grapple(_Powerup):
    SPRITE = 'grappleicon.ika-sprite'
    
    def apply(self):
        engine.saveData['grapple'] = True