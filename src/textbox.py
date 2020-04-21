import ika
import controls
import system

import engine
import entity

from xi import gui
from xi.misc import wrapText
#from xi.scrolltext import scrollableTextFrame
import xi.effects


#controls.init()

__portraits = {
}

def getPortrait(name):
    if name in __portraits:
        return __portraits[name]
    else:
        fileName = 'gfx/portrait_%s.png' % name
        img = ika.Image(fileName)
        __portraits[name] = img
        return img

class Tinter(object):
    def __init__(self):
        self.curTint = 0
        self.tint = 0
        self.time = 0

    def draw(self):
        self.curTint += self.curTint < self.tint
        self.curTint -= self.curTint > self.tint

        if self.curTint:
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, ika.RGB(0, 0, 0, self.curTint), True)

tint = Tinter()

crap = [tint] # crap to draw along with the map

def draw():
    ika.Map.Render()
    for c in crap:
        c.draw()

#------------------------------------------------------------------------------

def createTextBox(where, txt):
    # where is either a point or an entity
    WIDTH = 200
    width = WIDTH
    text = wrapText(txt, width, gui.default_font)
    width = max([gui.default_font.StringWidth(s) for s in text])
    height = len(text) * gui.default_font.height
    x, y = (0, 0)
    automove = True #automatic moving of where to display the box

    if isinstance(where, (tuple, list)):
        x, y = where

    if isinstance(where, entity.Entity):
        where = where.ent

    if isinstance(where, ika.Entity):
        ent = where
        x, y = ent.x + ent.hotwidth / 2 - ika.Map.xwin, ent.y - ika.Map.ywin
    else:
        x, y = where
        automove = False


    if automove and x < ika.Video.xres / 2:
        x -= width / 2

    width = WIDTH
    if x + width + 16 > ika.Video.xres:
        text = wrapText(txt, ika.Video.xres - x - 16, gui.default_font)
        width = max([gui.default_font.StringWidth(s) for s in text])
        height = len(text) * gui.default_font.height

    frame = gui.Frame()
    frame.addChild(gui.ScrollableTextLabel(text=text))
    frame.autoSize()

    if automove:
        if y > ika.Video.yres / 2:
            y += 32
        else:
            y -= frame.height + 16

    frame.position = x, y
    return frame

#------------------------------------------------------------------------------

class TextBox(object):
    def __init__(self, where, portrait, text):
        self.frame = createTextBox(where, text)

        if portrait is not None:
            self.img = getPortrait(portrait)
        else:
            self.img = None

    def update(self):
        pass

    def draw(self):
        if self.img is not None:
            if self.frame.x < ika.Video.xres / 2:
                ika.Video.Blit(self.img, 0, ika.Video.yres - self.img.height)
            else:
                ika.Video.ScaleBlit(self.img, ika.Video.xres, ika.Video.yres - self.img.height, -self.img.width, self.img.height)

        self.frame.draw()

def text(where, *args):
    """Displays a text frame.

    Where can be either a point or an entity.
    TODO: update Things while the textbox is visible
    """
    portrait, text = None, ''

    if len(args) == 1:
        text = args[0]

    elif len(args) == 2:
        portrait, text = args

    else:
        assert False, 'text recieves 1 or two arguments.'

    textBox = TextBox(where, portrait, text)

    engine.things.append(textBox)

    try:
        engine.beginCutScene()
        while not controls.attack1():
            engine.tick()
            engine.draw()

    finally:
        engine.endCutScene()
        engine.things.remove(textBox)

#------------------------------------------------------------------------------

def animate(ent, frames, delay, thing=None, loop=True, portrait=None, text=None):
    class AnimException(Exception):
        pass
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(ent, text)
        crap.append(text)
    try:
        while True:
            for frame in frames:
                ent.specframe = frame
                d = delay
                while d > 0:
                    d -= 1
                    draw()
                    ika.Video.ShowPage()
                    ika.Delay(1)
                    ika.Input.Update()
                    if controls.attack():
                        loop = False
                        raise AnimException
            if not loop:
                raise AnimException
    except:  #except what?
        if thing:
            crap.remove(thing)
        if text:
            crap.remove(text)
        ent.specframe = 0
