'''Earthquake. :D
'''

import ika
import engine
import sound

class Quake(object):

    def __init__(self, duration, x=2, y=None):
        self.duration = duration
        self.x = x
        self.y = y or x
        self.time = ika.GetTime() + duration

        self.wasLocked = engine.camera.locked
        
        sound.earthquake.Play()

    def update(self):
        
        if ika.GetTime() > self.time:
            engine.camera.locked = self.wasLocked
            sound.earthquake.Pause()
            return True
        else:
            engine.camera.locked = False
            engine.camera.center()

            ika.Map.xwin += ika.Random(-self.x, self.x)
            ika.Map.ywin += ika.Random(-self.y, self.y)

    def draw(self):
        pass
