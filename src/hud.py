import ika
import engine
from thing import Thing


shell = ika.Image("gfx/ui/icon_seashell.png")

def sgn(i):
    if i > 0:
        return 1
    if i < 0:
        return -1
    return 0


class Fader(Thing):
    
    def __init__(self):
        self.oldVal = self.oldMax = 0
        self.opacity = 0
        self.fadeIn = False

    def update(self):
        v = sgn(int(self.curVal - self.oldVal))
        m = sgn(int(self.curMax - self.oldMax))

        if self.fadeIn:
            self.opacity = min(512, self.opacity + 20)
            if self.opacity == 512:
                self.fadeIn = False

        if not v and not m:  # if neither has changed
            self.opacity = max(0, self.opacity - 1)
        else:
            self.fadeIn = True
            self.oldVal += v
            self.oldMax += m
            
    curVal = property()
    curMax = property()


class VerticalGauge(Fader):

    def __init__(self, imageName, x, y, justify='bottom',
                 colour=ika.RGB(255, 255, 255)):
        """imageName - name of the image series to use.
           (ie 'gfx/ui/hud_%sbar.png')
           x, y are position
           justify is either 'top' or 'bottom'
        """
        
        super(VerticalGauge, self).__init__()
        
        (self.span, self.top, self.bottom) = [
            ika.Image("gfx/ui/hud_%s%s.png" % (imageName, ['bar','top','bot'][i])) for i in range(3)
        ]
        self.x, self.y = x,y
        self.justify = justify.lower()
        self.colour = ika.GetRGB(colour)[:-1]
        self.height = None

    def draw(self):
        if self.opacity == 0:
            return
        o = min(255, self.opacity)
        # the heightof the repeated span image thingo.
        # each end of the gauge occupies two pixels, so we subtract four.
        # (bad hack, I know)
        height = min(226, (self.height or self.oldMax) - self.top.height - self.bottom.height)
        if self.justify == 'top':
            y = self.y + self.top.height
        else:
            y = (ika.Video.yres - height - self.top.height - self.bottom.height -
                 self.y)
        ika.Video.TintBlit(self.top, self.x, y, ika.RGB(255, 255, 255, o))
        ika.Video.TintBlit(self.bottom, self.x, y + height + self.top.height,
                           ika.RGB(255, 255, 255, o))
        y += self.top.height
        ika.Video.ClipScreen(0, y, ika.Video.xres, y + height)
        for Y in range(0, height, self.span.height):
            ika.Video.TintBlit(self.span, self.x, y + Y,
                               ika.RGB(255, 255, 255, o))
        ika.Video.ClipScreen()
            
        if self.oldVal:
            c = self.colour
            va = self.oldVal
            #print `self.curVal`
            for a in range(self.oldVal / 226 + 1):
                v = min(226, va) * height / min(226, self.oldMax)
                if self.justify == 'top':
                    self.drawRect(self.x + 5, y, self.x + 7, y + v, o, col=c)
                else:
                    self.drawRect(self.x + 5, y + height - v,
                                  self.x + 7, y + height - 1, o, col=c)
                va -= 226
                c = (c[0], c[1]+128, c[2])


    def drawRect(self, x, y, w, h, opacity, col=None):
        """Used to draw in the filled part of the gauge."""
        if not col:
            col = self.colour
        ika.Video.DrawRect(x, y, w, h, ika.RGB(*(col + (opacity,))),
                           True)
                           
                           
class HorizontalGauge(Fader):

    def __init__(self, imageName, x, y, justify='left',
                 colour=ika.RGB(255, 255, 255)):
        """imageName - name of the image series to use.
           (ie 'gfx/ui/hud_%sbar.png')
           x, y are position
           justify is either 'left' or 'right'
        """
        
        super(HorizontalGauge, self).__init__()
        
        (self.span, self.left, self.right) = [
            ika.Image("gfx/ui/hud_%s%s.png" % (imageName, ['bar','left','right'][i])) for i in range(3)
        ]
        self.x, self.y = x,y
        self.justify = justify.lower()
        self.colour = ika.GetRGB(colour)[:-1]
        self.width = None

    def draw(self):
        if self.opacity == 0:
            return
        o = min(255, self.opacity)
        # the width of the repeated span image thingo.
        # each end of the gauge occupies two pixels, so we subtract four.
        # (bad hack, I know)
        width = (self.width or self.oldMax) - 4
        if self.justify == 'left':
            x = self.x + 2
        else:
            x = (ika.Video.xres - width - self.left.width - self.right.width -
                 self.x - 2)
        ika.Video.TintBlit(self.left, x, self.y, ika.RGB(255, 255, 255, o))
        ika.Video.TintBlit(self.right, x + width + self.left.width, self.y,
                           ika.RGB(255, 255, 255, o))
        x += self.left.width
        ika.Video.ClipScreen(x, 0, x + width + 1, ika.Video.yres)
        for X in range(0, width-1, self.span.width):
            ika.Video.TintBlit(self.span, x + X, self.y,
                               ika.RGB(255, 255, 255, o))
        ika.Video.ClipScreen()
        x -= 2
        if self.width:
            v = self.oldVal * self.width / self.oldMax
        else:
            v = self.oldVal
        if self.oldVal:
            if self.justify == 'left':
                self.drawRect(x, self.y + 5, x + v, self.y + 6, o)
            else:
                self.drawRect(x + (self.width or self.oldMax) - v, self.y + 5,
                              x + (self.width or self.oldMax), self.y + 6, o)

    def drawRect(self, x, y, w, h, opacity):
        """Used to draw in the filled part of the gauge."""
        ika.Video.DrawRect(x, y, w, h, ika.RGB(*(self.colour + (opacity,))),
                           True)




class HPBar(VerticalGauge):

    def __init__(self):
        super(HPBar, self).__init__('hp', 0, 0,
                                    justify='bottom')
        self.x = 0
        self.colour = (255, 0, 0)

    curVal = property(lambda self: engine.player.stats.hp)
    curMax = property(lambda self: engine.player.stats.maxhp)


class EXPBar(VerticalGauge):

    def __init__(self):
        super(EXPBar, self).__init__('mp', 0, 0,
                                    justify='bottom')
        self.x = ika.Video.xres - self.top.width
        self.height = 210
        self.colour = (0, 255, 0)
        self.oldMax = self.curMax
        self.oldVal = self.curVal

    curVal = property(lambda self: engine.player.stats.exp * self.height / 100)
    curMax = property(lambda self: self.height)


"""class EXPBar(HorizontalGauge):

    def __init__(self):
        super(EXPBar, self).__init__('exp', 0, 0,
                                     justify='left')
        self.width = ika.Video.xres / 2
        self.x = (ika.Video.xres - self.width) / 2 - 4
        self.y = ika.Video.yres - self.span.height
        self.colour = (0, 255, 128)
        self.oldMax = self.curMax
        self.oldVal = self.curVal

    def drawRect(self, x, y, w, h, opacity):
        super(EXPBar, self).drawRect(x, y, w, h - 1, opacity)

    curVal = property(lambda self: engine.player.stats.exp * self.width /
                                   engine.player.stats.next)
    curMax = property(lambda self: self.width)"""


class ShellsIndicator(Fader):
    
    def __init__(self):
        super(ShellsIndicator, self).__init__()
        self.oldMax = self.curMax
        self.oldVal = self.curVal        
        
    def draw(self):
        if self.opacity == 0:
            return
        o = min(255, self.opacity)
        ika.Video.TintBlit(shell, self.x - shell.width, self.y, ika.RGB(255, 255, 255, o))
        engine.font.Print(self.x, self.y + self.yofs, "#[%02XFFFFFF] x %i" % (o, engine.player.stats.money))
    
    x = property(lambda self: ika.Video.xres - 5 - engine.font.StringWidth(" x %i" % engine.player.stats.money))
    y = property(lambda self: 5)
    yofs = property(lambda self: shell.height - engine.font.height)
        
    curVal = property(lambda self: engine.player.stats.money)
    curMax = property(lambda self: 999999)        