import ika
import engine
from thing import Thing


MAXIMUM_OPACITY = 255


class Caption(Thing):

    def __init__(self, text, x=None, y=None, duration=200):
        super(Caption, self).__init__()
        font = engine.font
        width = font.StringWidth(text)
        height = font.height
        self.x = x or (ika.Video.xres - width) / 2
        self.y = y or ika.Video.yres - height - 40
        canvas = ika.Canvas(width, height)
        canvas.DrawText(font, 0, 0, text)
        self.img = ika.Image(canvas)
        self.opacity = 0
        self.duration = duration
        self.update = self._update().next

    def _update(self):
        while self.opacity < MAXIMUM_OPACITY:
            self.opacity += 2
            yield None
        while self.duration > 0:
            self.duration -= 1
            yield None
        while self.opacity > 0:
            self.opacity -= 2
            yield None
        yield True

    def draw(self):
        ika.Video.TintBlit(self.img, self.x, self.y,
                           ika.RGB(255, 255, 255,
                                   min(self.opacity, MAXIMUM_OPACITY)))
