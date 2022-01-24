'''GUI elements that are not a part of xi proper, but are widely useful anyway.
'''

import ika
import controls
import sound
from xi import gui, layout
from xi.menu import Cancel



def init(font, wnd=None, csr=None):
    '''Initializes defaults for the GUI system.  This MUST be called
       before creating any instances.
    '''
    global default_font, default_window, default_cursor
    default_font = font
    default_window = wnd
    default_cursor = csr


class TextFrame(gui.Frame):
    '''A frame with text in it.  This is a simple convenience class,
       combining the Frame and StaticText controls into a single
       convenient object.
    '''
    def __init__(self, x=0, y=0, width=0, height=0, *args, **kwargs):
        super(TextFrame, self).__init__(x, y, width, height, *args, **kwargs)
        # way cool.  since keyword arguments are passed on, the font will be
        # set properly.  additionally, text will be added just like StaticText.
        # Consistency totally rules.
        self.__text = gui.StaticText(0, 0, width, height, *args, **kwargs)
        self.addChild(self.__text)
        self.autoSize()

    def getText(self):
        return self.__text.text

    def setText(self, value):
        self.__text.setText(value)

    def getFont(self):
        return self.__text.font

    def setFont(self, font):
        self.__text.font = font

    text = property(
        fget=getText,
        fset=setText,
        doc='Gets or sets the text contained by the control.'
    )

    font = property(
        fget=getFont,
        fset=setFont,
        doc='Gets or sets the font used for the text contained by the control.'
    )

    def addText(self, *args):
        '''Appends text to what is already contained.'''
        self.text.addText(*args)

    def autoSize(self):
        '''Autosizes the frame such that it is just large enough to
           contain its text.
        '''
        self.__text.autoSize()
        self.size = self.__text.size


class ScrollableTextFrame(gui.ScrollableTextLabel):
    def __init__(self, *args, **kwargs):
        super(ScrollableTextFrame, self).__init__(self, *args, **kwargs)

        self.window = kwargs.get('window', gui.default_window)
        self.border = self.window.border * 2

    def draw(self, x=0, y=0):
        self.window.draw(x, y, self.width, self.height)
        super(ScrollableTextFrame, self).draw(x, y)


class IconTableWindow(gui.Frame):

    def __init__(self, *args, **kw):
        super(IconTableWindow, self).__init__(*args, **kw)

        self.items = []
        
        self.iconWidth = 16
        self.iconHeight = 16

        self.cursor = ika.Image('gfx/ui/hud_box.png')
        self.cursorPos = 0

        self.layout = self.createLayout()
        
        self.addChild(self.layout)
        
    def createLayout(self):
        return layout.FlexGridLayout(cols=8, pad=0)

    def createContents(self):

        contents = []
        
        for img in self.icons:
            contents.append(gui.Picture(image=img, width=self.iconWidth, height=self.iconHeight))

        while len(contents) < 8:
            contents.append(layout.Spacer())
        
        return contents

    def addIcon(self, iconName, iconImg):
        self.icons.append((iconName, iconImg))
        
    def drawCursor(self, active=False):
        pic = self.layout.children[self.cursorPos]

        WIDTH = 4
        x = pic.x + self.x + self.layout.x - WIDTH
        y = pic.y + self.y + self.layout.y - WIDTH

        BLINK_RATE = 50
        blink = (ika.GetTime() % BLINK_RATE) * 2 > BLINK_RATE

        if active and blink:
            ika.Video.Blit(self.cursor, x, y)
        else:
            ika.Video.TintBlit(self.cursor, x, y, ika.RGB(128, 128, 128))

    def update(self):
        
        oldPos = self.cursorPos
        
        if controls.left.pressed or controls.ui_left.pressed or controls.joy_left.pressed:
            self.cursorPos = max(0, self.cursorPos - 1)
        elif controls.right.pressed or controls.ui_right.pressed or controls.joy_right.pressed:
            self.cursorPos = min(len(self.icons) - 1, self.cursorPos + 1)
        elif (controls.down.pressed or controls.ui_down.pressed or controls.joy_down.pressed) and self.cursorPos < len(self.items) - 8:
            self.cursorPos += 8
        elif (controls.up.pressed or controls.ui_up.pressed or controls.joy_up.pressed) and self.cursorPos > 7:
            self.cursorPos -= 8

        elif controls.attack1.pressed or controls.joy_attack1.pressed or controls.ui_accept.pressed:
            # have to use pressed and not position here, because the other menu eats it
            return self.select(self.cursorPos)
            
        elif controls.cancel.pressed or controls.joy_cancel.pressed or controls.ui_cancel.pressed:
            return Cancel
            
        if self.cursorPos != oldPos:
            sound.menuMove.Play()

        return None

    def select(self, cursorPos):
        sound.menuSelect.Play()
        return cursorPos# TODO someday: have items that can be used from the subscreen?
        
    icons = property(lambda self: [x.icon for x in self.items])