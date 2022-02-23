
import ika
import engine
from textbox import text, textMenu
from clouds import Clouds, ClippedClouds
from quake import Quake
from sound import playMusic, killMusic, switch
from enemy import Enemy
from thing import Thing
import effects

from engine import delay, draw, tick
from shop import *
import sound

def exitTo(destMap, offsetFrom, offsetTo, otherCoord, axis='x'):
    offsetFrom *= 16
    offsetTo *= 16
    otherCoord *= 16

    def doX():
        x = engine.player.x - offsetFrom + offsetTo
        engine.mapSwitch(destMap, (x, otherCoord))

    def doY():
        y = engine.player.y - offsetFrom + offsetTo
        engine.mapSwitch(destMap, (otherCoord, y))

    if axis == 'x':
        return doX
    elif axis == 'y':
        return doY
    else:
        raise Exception, 'This should never happen!  axis = ' + repr(axis)


def toggleBlocks():

    b1 = ika.Map.FindLayerByName('B1')
    b2 = ika.Map.FindLayerByName('B2')
    cx = (engine.player.x + engine.player.ent.hotwidth / 2) / ika.Tileset.width
    cy = (engine.player.y + engine.player.ent.hotheight / 2) / ika.Tileset.height

    if engine.player.ent.mapobs and ika.Map.GetTile(cx, cy, b2) == 183:

        for tx in range(ika.Map.width / ika.Tileset.width):
            for ty in range(ika.Map.height / ika.Tileset.height):
                if ika.Map.GetTile(tx, ty, b1) == 127:
                    curtile = ika.Map.GetTile(tx, ty, b2)
                    curobs = ika.Map.GetObs(tx, ty, b2)
                    ika.Map.SetTile(tx, ty, b2, 126 - curtile)
                    ika.Map.SetObs(tx, ty, b2, curobs^1)

        ika.Map.SetTile(cx, cy, b2, 191)

        switch.Play()


def resetSwitch():

    cx = (engine.player.x + engine.player.ent.hotwidth / 2) / ika.Tileset.width
    cy = (engine.player.y + engine.player.ent.hotheight / 2) / ika.Tileset.height
    b2 = ika.Map.FindLayerByName('B2')

    if ika.Map.GetTile(cx, cy, b2) not in [183, 191]:

        for tx in range(ika.Map.width / ika.Tileset.width):
            for ty in range(ika.Map.height / ika.Tileset.height):
                if ika.Map.GetTile(tx, ty, b2) == 191:
                    ika.Map.SetTile(tx, ty, b2, 183)

def numEnemies():

    num = 0
    for e in engine.entities:
        if isinstance(e, Enemy):
            num += 1
    return num


def clearEnemies():
    for e in engine.entities:
        if isinstance(e, Enemy):
            engine.destroyEntity(e)
            

class NoEnemyListener(Thing):

    def __init__(self, pos, flag=None):
        self.pos = pos
        self.flag = flag


    def update(self):
        hadToClear = False
        if self.flag and self.flag in engine.saveData:
            hadToClear = True
            clearEnemies()
        if not numEnemies():
            for p in self.pos:
                l = ika.Map.FindLayerByName(p[2])
                ika.Map.SetObs(p[0], p[1], l, 0)
                ika.Map.SetTile(p[0], p[1], l, 0)
                sound.dooropen.Play()
            if self.flag and not hadToClear:
                engine.saveData[self.flag] = True
            return True

    def draw(self, *args):
        pass
        


def goodNight(): #stay at an inn!
    engine.beginCutScene()
    sound.fader.playandresume(sound.music['goodnight'], 250000)    
    effects.fadeOut(100, draw=engine.raw_draw)    
    delay(300, drawfunc='blank')    
    effects.fadeIn(100, draw=engine.raw_draw)
    engine.endCutScene()
    engine.player.stats.hp = engine.player.stats.maxhp



