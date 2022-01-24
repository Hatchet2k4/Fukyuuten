import ika
import controls
import effects
import sound
from menu import Cancel, Menu
from saveload import SaveGame

from xi import gui
from xi import cursor
from xi import layout

from gui import TextFrame


class SaveGameFrame(gui.Frame):

    def __init__(self, *args, **kw):
        super(SaveGameFrame, self).__init__(*args, **kw)
        self.save = kw.get('save', None)
        self.layout = layout.VerticalBoxLayout()
        self.addChild(self.layout)
        self.update(kw['icons'])

    def update(self, icons):
        if self.save:
            stats = self.save.stats
            self.layout.setChildren([
                layout.HorizontalBoxLayout(
                    gui.StaticText(text='HP%03i/%03i' %
                                   (stats.hp, stats.maxhp)),
                    layout.Spacer(width=16),
                    gui.StaticText(text='Lv. %02i' % stats.level)
                ),
                layout.FlexGridLayout(cols=4, children = (
                        gui.StaticText(text='Anastasia'),
                        layout.Spacer(),
                        layout.Spacer(),
                        gui.StaticText(text='Lv  %02i' % stats.level),
                        gui.StaticText(text='Att:%02i  ' % stats.att),
                        gui.StaticText(text='Mag:%02i  ' % stats.mag),
                        gui.StaticText(text='Def:%02i  ' % stats.pres),
                        gui.StaticText(text='Res:%02i  ' % stats.mres)
                    )
                )
            ])

            self.layout.layout()
            self.autoSize()
        else:
            raise Exception


class SaveLoadMenu(object):

    def __init__(self, saves, saving=False):
        super(SaveLoadMenu, self).__init__()

        self.icons = dict([
                (s, gui.Picture(image='gfx/ui/icon_%s.png' % s))
                for s in ('att', 'mag', 'pres', 'mres')
            ]
        )

        self.cursor = cursor.ImageCursor('gfx/ui/pointer.png')
        self.saves = saves
        boxes = [SaveGameFrame(save=s, icons=self.icons) for s in saves]

        if saving:
            boxes.append(TextFrame(text='Create New'))
        elif not boxes:
            boxes.append(TextFrame(text='No Saves'))

        self.layout = layout.VerticalBoxLayout(pad=16)
        self.layout.setChildren(boxes)
        self.layout.layout()
        self.cursorPos = 0
        self.oldY = 0  # current offset
        self.curY = 0  # offset we should be at

        if boxes:
            self.wndHeight = boxes[0].height + 16
        else:
            self.wndHeight = 0  # What should we do here?

        self.layout.x = 16  # doesn't change

    def draw(self):
        self.layout.y = (ika.Video.yres - self.wndHeight) / 2 - self.oldY + 16
        self.layout.draw()
        # cursor doesn't move, everything else does
        self.cursor.draw(16, ika.Video.yres / 2)

    def update(self):
        assert (len(self.layout.children),
                'There should be at least one frame in here. (Either '
                'indicating no saves, or to create a new save.)')
        ika.Input.Update()
        if self.curY < self.oldY:
            self.oldY -= 2
        elif self.curY > self.oldY:
            self.oldY += 2
        elif (controls.up.pressed or controls.ui_up.pressed or controls.joy_up.pressed) and self.cursorPos > 0:
           sound.menuMove.Play()
           self.cursorPos -= 1
           self.curY = self.cursorPos * self.wndHeight
        elif (controls.down.pressed or controls.ui_down.pressed or controls.joy_down.pressed) and \
             self.cursorPos < len(self.layout.children) - 1:
           sound.menuMove.Play()
           self.cursorPos += 1
           self.curY = self.cursorPos * self.wndHeight
        elif (controls.attack1() or controls.joy_attack1() or controls.ui_accept()):
            sound.menuSelect.Play()
            return self.cursorPos
        elif (controls.cancel() or controls.joy_cancel() or controls.ui_cancel()):
            return Cancel


def readSaves():
    saves = []
    try:
        i = 0
        while True:
            saves.append(SaveGame('save%i' % i))
            i += 1
    except IOError:
        return saves


def loadMenu(fadeOut=True):
    title = TextFrame(text='Load Game')
    title.position = (16, 16)
    saves = readSaves()
    m = SaveLoadMenu(saves, saving=False)

    def draw():
        ika.Video.ClearScreen()  # fix this
        m.draw()
        title.draw()

    effects.fadeIn(50, draw=draw)
    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()

    if fadeOut:
        effects.fadeOut(50, draw=draw)

    draw()
    if i is not Cancel and i < len(saves):
        return saves[i]


def saveMenu():
    title = TextFrame(text='Save Game')
    title.position = (16, 16)
    saves = readSaves()
    m = SaveLoadMenu(saves, saving=True)

    def draw():
        ika.Video.ClearScreen()  # fix this
        m.draw()
        title.draw()

    effects.fadeIn(50, draw=draw)
    i = None
    while i is None:
        i = m.update()
        draw()
        ika.Video.ShowPage()

    if i is not Cancel:
        s = SaveGame.currentGame()
        s.save('save%i' % i)

    effects.fadeOut(50, draw=draw)
