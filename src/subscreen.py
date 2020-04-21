
import ika

from xi import gui
from xi import cursor
from xi import layout
from xi.menu import Menu, Cancel
from xi.misc import wrapText
from xi.window import ImageWindow
from xi.transition import Transition, WindowMover

import engine
import effects
import config
import controls
import sound
import saveloadmenu

from gui import ScrollableTextFrame, IconTableWindow
from gameover import EndGameException

menuChoices = ['Resume',
               'Items',
               'Exit',
               ]
               
class Window(object):
    '''Specialized window.  Ghastly and hacked up to accomodate the awesome
    looking window frame thingie that corey drew.
    '''

    def __init__(self, nameTemplate):
        super(Window, self).__init__()

        self.iTopleft, self.iTopright, self.iBottomleft, self.iBottomright = [
            ika.Image(nameTemplate % i) for i in
            ('top_left', 'top_right', 'bottom_left', 'bottom_right')
        ]

        self.iLeft, self.iRight, self.iTop, self.iBottom = [
            ika.Image(nameTemplate % i) for i in
            ('left', 'right', 'top', 'bottom')
        ]

        self.Blit = ika.Video.ScaleBlit
        self.TintBlit = lambda img, x, y, w, h, c: ika.Video.TintDistortBlit(img, (x,y,c), (x+w,y,c), (x+w,y+h,c), (x,y+h,c))
        self.border = max(self.iLeft.width, self.iTop.height)

    def draw(self, x, y, w, h, c=ika.RGB(255,255,255,255)):
        b = self.left / 2
        x2 = x + w + b
        y2 = y + h + b
        x -= b
        y -= b
        
        mod = ika.GetRGB(c)[3]
        
        ika.Video.TintBlit(self.iTopright, x2, y - self.iTopright.height, c)
        ika.Video.TintBlit(self.iBottomleft, x - self.iBottomleft.width, y2, c)
        self.TintBlit(self.iLeft, x - self.iLeft.width, y, self.iLeft.width, y2 - y, c)
        self.TintBlit(self.iRight, x2, y, self.iRight.width, y2 - y, c)
        self.TintBlit(self.iTop, x, y - self.iTop.height, x2 - x, self.iTop.height, c)
        self.TintBlit(self.iBottom, x, y2, x2 - x, self.iBottom.height, c)
        ika.Video.DrawRect(x, y, x2, y2, ika.RGB(0,0,0,mod), True)

        # EVIL HARD CODED
        ax = 8
        ay = 12

        # These two need special treatment, 'cause they're shiny and huge
        ika.Video.TintBlit(self.iTopleft,  x - ax, y - ay, c)
        ika.Video.TintBlit(self.iBottomright, x2 - self.iBottomright.width + ax, y2 - self.iBottomright.height + ay, c)

    left   = property(lambda self: self.border)
    right  = property(lambda self: self.border)
    top    = property(lambda self: self.border)
    bottom = property(lambda self: self.border)

class SubScreenWindow(gui.Frame):

    def __init__(self, *args, **kw):
        super(SubScreenWindow, self).__init__(*args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)

    def createLayout(self):
        return layout.VerticalBoxLayout()

    def refresh(self):
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        self.autoSize()

class ShopWindow(gui.Frame):

    def __init__(self, *args, **kw):
        super(ShopWindow, self).__init__(*args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)

    def createLayout(self):
        return layout.VerticalBoxLayout()
        
    def refresh(self):
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        
class StatWindow(SubScreenWindow):

    def createContents(self):
        stats = engine.player.stats
        return (
            gui.StaticText(text='Anastasia'),
            gui.StaticText(text=''),
            gui.StaticText(text='Level:\t\t%03i' % stats.level),
            gui.StaticText(text=''),
            gui.StaticText(text='Experience: %03i%%' % stats.exp),
            gui.StaticText(text=''), 
            gui.StaticText(text='HP:\t%03i/%03i' % (stats.hp, stats.maxhp)),
            gui.StaticText(text=''),
            gui.StaticText(text='Attack:\t\t%03i' % stats.att),
            gui.StaticText(text='Magic:\t\t%03i' % stats.mag),
            gui.StaticText(text='Defense:\t\t%03i' % stats.pres),
            gui.StaticText(text='Resistance:\t%03i' % stats.mres),
            gui.StaticText(text=''),
            gui.StaticText(text='Seashells:\t%i' % stats.money)
        )


class AttribWindow(SubScreenWindow):

    def __init__(self):
        super(AttribWindow, self).__init__()

    def createContents(self):
        stats = engine.player.stats
        return (
            gui.StaticText(text='Attack:\t\t%03i' % stats.att),
            gui.StaticText(text='Magic:\t\t%03i' % stats.mag),
            gui.StaticText(text='Defense:\t\t%03i' % stats.pres),
            gui.StaticText(text='Resistance:\t%03i' % stats.mres)
        )


class ToolWindow(SubScreenWindow):

    #ITEM_NAMES = ('spear', 'sword', 'glove', 'grapple', 'petrify', 'wind', 'heal')
    #WEAPONS = ('spear', 'sword', 'glove')
    ITEM_NAMES = ('grapple',)
    WEAPONS = ('spear', 'sword')
    EQUIP = ('armor',)

    def __init__(self):
        super(ToolWindow, self).__init__()

        self.icons = {}

        self.cursor = ika.Image('gfx/ui/hud_box.png')
        self.cursorPos = 0

        self.layout2 = layout.FlexGridLayout(cols=len(self.WEAPONS + self.EQUIP + self.ITEM_NAMES), pad=4)

    def createLayout(self):
        return layout.VerticalBoxLayout(pad=0)

    def createContents(self):
        player = engine.player
        stats = player.stats

        size = 16, 16

        contents = []
        
        self.icons = {}
        
        for name in self.WEAPONS:
            item = engine.player.__dict__[name].item
            if item:
                self.icons[name] = item.icon
        
        for name in self.EQUIP:
            item = engine.player.__dict__[name]
            if item:
                self.icons[name] = item.icon
                
        for name in self.ITEM_NAMES:
            self.icons[name] = ika.Image("gfx/ui/icon_%s.png" % name)
            
        for name in self.WEAPONS + self.EQUIP + self.ITEM_NAMES:
            if (engine.saveData.get(name) is not None or name in self.WEAPONS + self.EQUIP) and name in self.icons:
                icon = self.icons[name]
                contents.append(gui.Picture(image=icon, width=size[0], height=size[1]))
            else:
                contents.append(layout.Spacer(width=size[0], height=size[1]))

        i = 0
        for name in self.WEAPONS + self.EQUIP + self.ITEM_NAMES:
            s = ''

            if name in self.icons:
                if name in self.WEAPONS:
                    if getattr(player, name) is player.weapon:
                        s = '*'
                elif name in self.EQUIP:
                    if getattr(player, name).item in [player.armor]:
                        s = '*'
                elif engine.saveData.get(name):
                    s = 'DSA123456789'[i]
                    i += 1
                    
            contents.append(gui.StaticText(text=s.center(3)))

        self.layout2.setChildren(contents)

        return (
            gui.StaticText(text='Tools'),
            self.layout2,
        )

    def drawCursor(self, active=False):
        pic = self.layout2.children[self.cursorPos]

        WIDTH = 4
        x = pic.x + self.x + self.layout2.x - WIDTH
        y = pic.y + self.y + self.layout2.y - WIDTH

        BLINK_RATE = 50
        blink = (ika.GetTime() % BLINK_RATE) * 2 > BLINK_RATE

        if active and blink:
            ika.Video.Blit(self.cursor, x, y)
        else:
            ika.Video.TintBlit(self.cursor, x, y, ika.RGB(128, 128, 128))

    def update(self):
        if controls.left.pressed:
            self.cursorPos = max(0, self.cursorPos - 1)
            return self.select(self.cursorPos)
            sound.menuMove.Play()

        elif controls.right.pressed:
            self.cursorPos = min(len(self.WEAPONS) - 1, self.cursorPos + 1)
            return self.select(self.cursorPos)
            sound.menuMove.Play()

            # have to use pressed and not position here, because the other menu eats it
            #return self.select(self.cursorPos)
        
        return False

    def select(self, cursorPos):
        player = engine.player

        name = self.WEAPONS[cursorPos]

        if name not in engine.saveData: return # can't use something you don't have

        sound.menuSelect.Play()

        if name in self.WEAPONS and name in self.icons and player.weapon is not getattr(player, name):
            if player.weapon:
                if player.weapon is player.spear and player.spear.item:
                    player.spear.item.deapplyAll(player)
                elif player.weapon is player.sword and player.sword.item:
                    player.sword.item.deapplyAll(player)
            player.weapon = getattr(player, name)
            if name == 'spear' and player.spear.item:
                player.spear.item.applyAll(player)
            elif name == 'sword' and player.sword.item:
                player.sword.item.applyAll(player)
            self.refresh()
            return True
        else:
            return # TODO someday: have items that can be used from the subscreen?


class MenuWindow(Menu):

    def __init__(self):
        super(MenuWindow, self).__init__(textctrl=gui.ScrollableTextLabel())
        self.addText(*menuChoices)
        self.autoSize()


class PauseScreen(object):

    def __init__(self):
        assert _initted
        super(PauseScreen, self).__init__()
        self.statWnd = StatWindow()
        self.toolWnd = ToolWindow()
        self.menu = MenuWindow()

        self.menuWindow = gui.Frame()
        self.menuWindow.addChild(self.menu)
        self.menuWindow.autoSize()

    def refresh(self):
        self.statWnd.refresh()
        self.statWnd.dockTop().dockLeft()
        self.toolWnd.refresh()
        self.toolWnd.dockBottom().dockRight()
        self.menuWindow.dockTop().dockRight()

    def show(self):
        TIME = 35
        self.refresh()

        t = Transition()

        t.addChild(self.statWnd,
            startRect=(-self.statWnd.right, self.statWnd.top),
            time=TIME
        )

        t.addChild(self.toolWnd,
            startRect=(ika.Video.xres, self.toolWnd.top),
            time=TIME
        )

        t.addChild(self.menuWindow,
            startRect=(ika.Video.xres, self.menuWindow.top),
            time=TIME
        )

        for i in range(TIME):
            t.update(1)
            o = i * 128 / TIME  # tint intensity for this frame
            engine.raw_draw()
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                               ika.RGB(0, 0, 0, o), True)
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

    def hide(self):
        TIME = 40
        t = Transition()

        t.addChild(
            self.statWnd,
            endRect=(-self.statWnd.right, self.statWnd.top),
            time=TIME
        )

        t.addChild(
            self.toolWnd,
            endRect=(ika.Video.xres, self.toolWnd.top),
            time=TIME
        )

        t.addChild(
            self.menuWindow,
            endRect=(ika.Video.xres, self.menuWindow.top),
            time=TIME
        )

        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 / TIME  # menu opacity for this frame
            engine.raw_draw()
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                               ika.RGB(0, 0, 0, o / 2), True)
            self.draw(o)
            ika.Video.ShowPage()
            ika.Input.Update()

    def draw(self, opacity=255):
        gui.default_window.opacity = opacity
        self.statWnd.draw()
        self.toolWnd.draw()
        self.menuWindow.draw()

        self.toolWnd.drawCursor(True)

    def run(self):
        self.show()
        while True:
            engine.raw_draw()

            ika.Video.DrawRect(
                0, 0, ika.Video.xres, ika.Video.yres,
                ika.RGB(0, 0, 0, 128), True
            )

            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()
            
            if self.menu.cursorPos == 2:
                toolResult = self.toolWnd.update()
                if toolResult:
                    self.refresh()
                
            result = self.menu.update()

            if result is None:
                continue

            elif result is Cancel or menuChoices[result] == 'Resume':
                self.hide()
                return

            elif menuChoices[result] == 'Items' and engine.player.items:
                self.hide()
                i = InventoryScreen()
                i.run()
                self.show()

            elif menuChoices[result] == 'Exit': # Exit
                self.hide()
                self.exitGame()
                return

        assert False, 'Execution should never reach this point.'

    def exitGame(self):
        # TODO: shiny fade out
        raise EndGameException

class InventoryScreen(object):

    def __init__(self):
        super(InventoryScreen, self).__init__()
        self.itemWnd = ItemWindow()
        self.descWnd = ItemDescWindow()
        self.moneyWnd = MoneyWindow()

    def refresh(self):
        self.itemWnd.refresh()
        self.itemWnd.dockTop().dockLeft()
        self.itemWnd.width = self.itemWnd.iconWidth * 8
        self.itemWnd.height = self.itemWnd.iconWidth * 12
        self.descWnd.refresh()
        self.descWnd.dockLeft(self.itemWnd).dockTop()
        self.descWnd.width = ika.Video.xres - self.descWnd.left - self.descWnd.border * 2
        self.descWnd.height = self.itemWnd.height
        self.descWnd.dockRight()
        self.descWnd.refresh()
        self.moneyWnd.refresh()
        self.moneyWnd.autoSize()
        self.moneyWnd.dockLeft(self.itemWnd).dockBottom()
        self.moneyWnd.width = self.descWnd.width
        self.moneyWnd.dockRight()

    def show(self):
        TIME = 35
        self.refresh()

        t = Transition()

        t.addChild(self.itemWnd,
            startRect=(-self.itemWnd.right, self.itemWnd.top),
            time=TIME
        )

        t.addChild(self.descWnd,
            startRect=(self.descWnd.left, -self.descWnd.bottom),
            time=TIME
        )

        t.addChild(self.moneyWnd,
            startRect=(self.moneyWnd.left, self.moneyWnd.bottom + self.moneyWnd.height),
            time=TIME
        )

        for i in range(TIME):
            t.update(1)
            o = i * 128 / TIME  # tint intensity for this frame
            engine.raw_draw()
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                               ika.RGB(0, 0, 0, o), True)
            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

    def hide(self):
        TIME = 40
        t = Transition()

        t.addChild(
            self.itemWnd,
            endRect=(self.itemWnd.left, ika.Video.yres + self.itemWnd.height),
            time=TIME
        )

        t.addChild(
            self.descWnd,
            endRect=(ika.Video.xres + self.descWnd.width, self.descWnd.top),
            time=TIME
        )

        t.addChild(
            self.moneyWnd,
            endRect=(ika.Video.xres + self.moneyWnd.width, self.moneyWnd.top),
            time=TIME
        )

        for i in range(TIME - 1, -1, -1):
            t.update(1)
            o = i * 255 / TIME  # menu opacity for this frame
            engine.raw_draw()
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                               ika.RGB(0, 0, 0, o / 2), True)
            self.draw(o)
            ika.Video.ShowPage()
            ika.Input.Update()

    def draw(self, opacity=255):
        gui.default_window.opacity = opacity
        self.itemWnd.draw()
        self.descWnd.draw()
        self.moneyWnd.draw()

        self.itemWnd.drawCursor(True)

    def run(self):
        self.refresh()
        self.show()
        while True:
            engine.raw_draw()

            ika.Video.DrawRect(
                0, 0, ika.Video.xres, ika.Video.yres,
                ika.RGB(0, 0, 0, 128), True
            )

            self.draw()
            ika.Video.ShowPage()
            ika.Input.Update()

            result = self.itemWnd.update()

            cursorPos = self.itemWnd.cursorPos
            self.descWnd.item = self.itemWnd.items[cursorPos]
            
            self.descWnd.refresh()
            
            if result is None:
                continue
            elif result is Cancel:
                self.hide()
                return
            else:
                self.hide()
                item = self.itemWnd.items[result]
                if item.type == 'spear':
                    if engine.player.spear.item:
                        engine.player.items.append(engine.player.spear.item)
                        if engine.player.weapon is engine.player.spear:
                            engine.player.spear.item.deapplyAll(engine.player)
                    engine.player.spear.item = item
                    if engine.player.weapon is engine.player.spear:
                        engine.player.spear.item.applyAll(engine.player)
                    engine.player.items.remove(item)                
                elif item.type == 'sword':
                    if engine.player.sword.item:
                        engine.player.items.append(engine.player.sword.item)
                        if engine.player.weapon is engine.player.sword:
                            engine.player.sword.item.deapplyAll(engine.player)
                    engine.player.sword.item = item
                    if engine.player.weapon is engine.player.sword:
                        engine.player.sword.item.applyAll(engine.player)
                    engine.player.items.remove(item)
                elif item.type == 'armor':
                    if engine.player.armorItem:
                        engine.player.items.append(engine.player.armorItem)
                        engine.player.armorItem.deapplyAll(engine.player)
                    engine.player.armorItem = item
                    engine.player.armorItem.applyAll(engine.player)
                    engine.player.items.remove(item)                    
                return

        assert False, 'Execution should never reach this point.'
        
class ItemWindow(IconTableWindow):
    
    def __init__(self, *args, **kwargs):
        super(ItemWindow, self).__init__(*args, **kwargs)
        self.items = engine.player.items
        
    def refresh(self):
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        self.autoSize()
        
    def autoSize(self):
        if not self.icons:
            self.size = (self.iconWidth + self.client.border * 2, self.iconHeight + self.client.border * 2)
        else:
            super(ItemWindow,self).autoSize()


class ItemDescWindow(ShopWindow):

    def __init__(self, *args, **kw):
        super(ItemDescWindow, self).__init__(*args, **kw)
        self.item = None
    
    def createContents(self):
        
        if self.item:
            
            sellPrice = self.item.totalPrice / 2
            
            yellow = "#[FF00FFFF]"
            white = "#[FFFFFFFF]"
            red = "#[FFAAAAFF]"
            blue = "#[FFFFAAAA]"
            gold = "#[FFAAFFFF]"
            green = "#[FFAAFFAA]"
                
            attribsLabel = gui.ColumnedTextLabel(columns=1, pad=10)
            [attribsLabel.addText('%s%s' % (blue, `a`)) for a in self.item.attribs]
            attribsLabel.addText('%sSell Price:%s %i' % (gold, white, sellPrice))
            attribsLabel.autoSize()
            
            dormantLabel = gui.ColumnedTextLabel(columns=1, pad=10)
            
            if self.item.dormant:
                [dormantLabel.addText('%s%s' % (green, `a`)) for a in self.item.dormant]
            else:
                dormantLabel.addText('None')
            dormantLabel.autoSize()
            
            descText = wrapText(self.item.desc, self.width, gui.default_font)
            for i in range(len(descText)):
                descText[i] = '%s%s' % (white, descText[i])
            
            return [ gui.StaticText(text='%s%s' % (yellow, self.item.name)),
                     gui.ScrollableTextLabel(text=descText),
                     gui.StaticText(text=''),
                     attribsLabel,
                     gui.StaticText(text=''),
                     gui.StaticText(text='%sDormant Attributes:' % green),
                     dormantLabel,
                     ]
        else:
            return []
            
class MoneyWindow(ShopWindow):

    def __init__(self):
        super(MoneyWindow, self).__init__()
        self.amount = engine.player.stats.money
    
    def createLayout(self):
        return layout.HorizontalBoxLayout(pad=4)
        
    def createContents(self):
        self.text = gui.StaticText(text=`self.amount`)
        return [ gui.Picture(image="gfx/items/icon_seashell.png"), self.text ]
        
    def refresh(self):
        super(MoneyWindow, self).refresh()
        self.text.y += 2
        
_initted = False

def init():
    global _initted
    _initted = True
    gui.init(
        font=ika.Font(config.FONT),
        window=Window('gfx/ui/win_%s.png'),
        cursor=cursor.ImageCursor('gfx/ui/pointer.png', hotspot=(14, 6))
    )
