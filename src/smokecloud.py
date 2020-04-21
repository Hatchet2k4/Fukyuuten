'''Thingie that displays a death cloud over an enemy when they die.
'''

import ika
import engine

from powerup import *

smoke = []
for s in range(1,6):
    smoke.append(ika.Image("gfx/smoke%i.png" % s))
    
class SmokeCloud(object):

    def __init__(self, mapX, mapY, width, height, ent, tint=ika.RGB(255, 255, 255)):
        self.curPos = 0
        self.speed = 7
        self.x = mapX
        self.y = mapY
        self.w = width
        self.h = height
        self.ent = ent
        self.tint = tint
        self.timer = 0

    def update(self):

        if self.ent is not None and self.ent.ent is not None:
                
            self.timer += 1
            
            if self.timer >= self.speed:
                self.curPos += 1
                self.timer = 0
                
            if self.curPos == 2 and not self.timer:
                self.ent.x = -1000
                self.generatePowerup(self.ent)
                
            if self.curPos >= len(smoke):
                engine.destroyEntity(self.ent)
                return True
        
        else:
            return True

    def draw(self):
        x = int(self.x - ika.Map.xwin)
        y = int(self.y - ika.Map.ywin)

        ika.Video.ScaleBlit(smoke[self.curPos], x, y, self.w, self.h)
        
    def generatePowerup(self, enemy):
        
        drop = None
        chance = ika.Random(0,100)
        kwargs = {}
        
        if enemy.powerup:
            
            drop = enemy.powerup
            
        elif chance > 50:
            
            #if chance > 98:
            #    drop = Skull
            #elif chance > 95:
            #    drop = GoldenEgg
            #elif chance > 92:
            #    drop = BlackPearl
            
            if chance > 93:
                drop = GreenBerry
            elif chance > 75:
                drop = RedBerry
            else:
                drop = Seashell
                kwargs['money'] = self.ent.stats.money
                
        if drop:
            x = self.x + self.w/2 - 8
            y = self.y + self.h/2 - 8            
            ent = ika.Entity(x, y, self.ent.layer, drop.SPRITE)
            engine.addEntity(drop(ent, **kwargs))
