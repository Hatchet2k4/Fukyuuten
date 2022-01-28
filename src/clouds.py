'''Thingie that displays clouds overhead.
'''

import ika
import engine

class Clouds(object):
    def __init__(self, imageName, speed=(0.2, 0.05), tint=ika.RGB(255, 255, 255)):
        self.image = ika.Image(imageName)
        self.pos = [0.0, 0.0]
        self.speed = speed
        self.tint = tint
        #self.speed = (0.0, 0.1)

    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self):
        x = int(self.pos[0] + ika.Map.xwin) % self.image.width
        y = int(self.pos[1] + ika.Map.ywin) % self.image.height

        ika.Video.TintTileBlit(self.image, -x, -y, ika.Video.xres * 2 + x, ika.Video.yres * 2 + y, self.tint)


class ClippedClouds(object):
    def __init__(self, imageName, speed=(0.2, 0.05)):
        self.image = ika.Canvas(imageName)   #ika.Image(imageName)
        self.pos = [0.0, 0.0]
        self.speed = speed
        self.canvas = ika.Canvas(320,240)
        #self.speed = (0.0, 0.1)

    def update(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self):
        x = int(self.pos[0] + ika.Map.xwin) % self.image.width
        y = int(self.pos[1] + ika.Map.ywin) % self.image.height
        self.canvas.Clear()

        self.image.TileBlit(self.canvas, -x, -y, ika.Video.xres * 2 + x, ika.Video.yres * 2 + y) 
        
        engine.stencil.Blit(self.canvas,0,0,ika.SubtractBlend)
        img = ika.Image(self.canvas)
        
        ika.Video.Blit(img, 0, 0)

        #ika.Video.TintTileBlit(self.image, -x, -y, ika.Video.xres * 2 + x, ika.Video.yres * 2 + y, self.tint)

