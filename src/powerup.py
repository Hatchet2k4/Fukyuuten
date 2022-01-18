import engine
import sound
import animator
from entity import Entity
from caption import DamageCaption

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
        self.flagName = ent.name
        
        if self.flagName.startswith('perm') and self.flagName in engine.saveData:
            self.remove()
        self.sound = sound.powerup #default sound

    def apply(self):
        pass

    def remove(self):
        self.x = self.y = -100  # hack!
        engine.destroyEntity(self)        

    def update(self):
        self.animate()
        if self.touches(engine.player):
            self.apply()
            engine.destroyEntity(self)
            self.sound.Play()

def createKey1(entity):
    return Key1(entity)
    
class Key1(_Powerup):
    SPRITE = 'key.ika-sprite'    
    def apply(self):
        engine.saveData[self.flagName] = 'True'
            
class Key2(_Powerup):
    SPRITE = 'key.ika-sprite'    
    def apply(self):
        engine.saveData[self.flagName] = 'True'

class Key3(_Powerup):
    SPRITE = 'key.ika-sprite'    
    def apply(self):
        engine.saveData[self.flagName] = 'True'        

def createRedBerry(entity):
    return RedBerry(entity)

class RedBerry(_Powerup):
    SPRITE = 'berry.ika-sprite'

    def apply(self):
        engine.player.stats.hp += 10

def createGreenBerry(entity):
    return GreenBerry(entity)

class GreenBerry(_Powerup):
    SPRITE = 'berry2.ika-sprite'
    
    def apply(self):
        engine.player.stats.hp += 40    

def createShell(entity):
    return Seashell(entity, money=1)

    
class Seashell(_Powerup):
    SPRITE = 'seashell.ika-sprite'
    
    def apply(self):
        if self.flagName.startswith('perm'):
            engine.saveData[self.flagName] = 'True'
        engine.player.stats.money += self.kwargs['money']
        #print `engine.player.stats.money`
        
def createPearl(entity):
    return BlackPearl(entity)
    
class BlackPearl(_Powerup):
    SPRITE = 'pearl.ika-sprite'
    
    def apply(self):
        if self.flagName.startswith('perm'):
            engine.saveData[self.flagName] = 'True'
        engine.player.stats.att += 1
        
def createEgg(entity):
    return GoldenEgg(entity)
    
class GoldenEgg(_Powerup):
    SPRITE = 'egg.ika-sprite'
    
    def apply(self):
        if self.flagName.startswith('perm'):
            engine.saveData[self.flagName] = 'True'    
        engine.player.stats.pres += 1
        engine.addThing(DamageCaption('Def +1', self.ent.x, self.ent.y, 80, 241, 156, 73))     
        
def createSkull(entity):
    return Skull(entity)
    
class Skull(_Powerup):
    SPRITE = 'skull.ika-sprite'
    
    def apply(self):
        if self.flagName.startswith('perm'):
            engine.saveData[self.flagName] = 'True'    
        pass 
        
    
class Grapple(_Powerup):
    SPRITE = 'grappleicon.ika-sprite'
        
    def apply(self):    
        self.sound = sound.NullSound() #prevent normal powerup sound from playing        
        engine.saveData['grapple'] = True
        engine.addThing(DamageCaption('Got Grapple', self.ent.x, self.ent.y, 80, 241, 156, 73))     
        sound.fader.playandresume(sound.music['victory'], 250000)        
        