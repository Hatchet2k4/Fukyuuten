# Basic cursor classes
# Coded by Andy Friesen
# Copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.

import ika

# base class (abstract)
class Cursor(object):
    '''
    Base cursor class.  Sort-of abstract,
    it can be used on its own as a null-cursor.
    '''
    def __init__(self, width, height, hotspot):
        self.__width = width
        self.__height = height
        self.__hotspot = hotspot

    def getWidth(self):
        return self.__width
    width = property(getWidth)

    def getHeight(self):
        return self.__height
    height = property(getHeight)

    def getSize(self):
        return self.__width, self.__height
    size = property(getSize)

    def getHotspot(self):
        return self.__hotspot
    def setHotspot(self, (x, y)):
        self.__hotspot = int(x), int(y)
    hotspot = property(getHotspot, setHotspot)

    def draw(self, x, y):
        pass

# just an alias
NullCursor = Cursor

# Basic cursor class that uses a font string as a cursor
class TextCursor(Cursor):
    def __init__(self, font, t = '>'):
        width = font.StringWidth(t)
        height = font.height
        hotspot = width, height / 2

        Cursor.__init__(self, width, height, hotspot)

        c = ika.Canvas(self.width, self.height)
        c.DrawText(font, 0, 0, t)
        self._img = ika.Image(c)

    def draw(self, x, y):
        ika.Video.Blit(self._img, x - self.hotspot[0], y - self.hotspot[1])

class ImageCursor(Cursor):
    def __init__(self, img, hotspot = None):
        if isinstance(img, (str, ika.Canvas)):
            img = ika.Image(img)
        elif not isinstance(img, ika.Image):
            assert False, 'image argument must be an image, a canvas, or a string.'

        if hotspot is None:
            hotspot = img.width, img.height / 2

        Cursor.__init__(self, img.width, img.height, hotspot)

        self._img = img

    def draw(self, x, y):
        ika.Video.Blit(self._img, x - self.hotspot[0], y - self.hotspot[1])

class AnimatedCursor(Cursor):
    def __init__(self, frames, delay = 10, hotspot = None):
        assert len(frames) > 0, 'Need at least one animation frame. ;P'

        width = frames[0].width
        height = frames[0].height
        hotspot = hotspot or (width, height / 2)
        Cursor.__init__(self, width, height, hotspot)

        self._delay = delay
        self._frames = frames

    def draw(self, x, y):
        frame = ika.GetTime() / self._delay

        ika.Video.Blit(self._frames[frame % len(self._frames)],
            x - self._hotspot[0], y - self._hotspot[1])

    # static method to create a cursor by cutting frames out of one
    # big image (vertical strip)
    def createFromImageStrip(canvas, numFrames, width, height, delay = 10, hotspot = None):
        assert canvas.height % numFrames == 0, \
            "Image's height is not an even multiple of the number of frames."

        frames = [None] * numFrames
        # cut up the canvas, and create our images
        for i in range(numFrames):
            c = ika.Canvas(width, height)
            canvas.Blit(c, 0, -(i * height), ika.Opaque)
            frames[i] = ika.Image(c)

        return AnimatedCursor(frames, delay, hotspot)

    createFromImageStrip = staticmethod(createFromImageStrip)
