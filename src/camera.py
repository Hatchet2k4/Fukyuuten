import ika
import engine
from thing import Thing


class Camera(Thing):

    def __init__(self):
        super(Camera, self).__init__()
        self.locked = False

    def update(self):
        if not self.locked:
            x = engine.player.x - ika.Video.xres / 2
            y = engine.player.y - ika.Video.yres / 2
            ika.Map.ywin += y > ika.Map.ywin
            ika.Map.ywin -= y < ika.Map.ywin
            ika.Map.xwin += x > ika.Map.xwin
            ika.Map.xwin -= x < ika.Map.xwin

    def center(self):
        ika.Map.xwin = engine.player.x - ika.Video.xres / 2
        ika.Map.ywin = engine.player.y - ika.Video.yres / 2
