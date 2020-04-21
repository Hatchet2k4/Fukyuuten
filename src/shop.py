'''GUI elements and other things used in shops. Mostly inherits from gui.py and xi.
'''

import ika
import engine
import controls
import item

from xi import gui, layout
from xi.transition import Transition, WindowMover
from xi.menu import Cancel, Menu
from xi.misc import wrapText

from gui import IconTableWindow


class ShopScreen(object):

    def __init__(self):
        super(ShopScreen, self).__init__()
        self.itemWnd = ItemWindow()
        self.descWnd = ItemDescWindow()
        self.moneyWnd = MoneyWindow()

    def refresh(self):
        self.itemWnd.refresh()
        self.itemWnd.dockTop().dockLeft()
        self.itemWnd.width = self.itemWnd.iconWidth * 8
        self.itemWnd.height = self.itemWnd.iconWidth * 12
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
            elif self.itemWnd.items[result].totalPrice <= engine.player.stats.money:
                self.hide()
                cs = ConstructScreen(self.itemWnd.items[result], self.descWnd.width)
                resultItem = cs.run()
                engine.player.items.append(resultItem)
                self.refresh()
                self.show()

        assert False, 'Execution should never reach this point.'
        
    def addItem(self, *args, **kw):
        for a in args:
            self.itemWnd.items.append(item.Item(a))
        self.itemWnd.refresh()

class ConstructScreen(object):

    def __init__(self, item, width):
        super(ConstructScreen, self).__init__()
        self.item = item
        self.consWndWidth = width
        self.consWnd = ItemConsWindow()
        self.consWnd.item = item
        self.consWnd.menu = DormantMenuWindow()
        self.consWnd.menu.item = item
        self.moneyWnd = MoneyWindow()

    def refresh(self):
        self.consWnd.width = self.consWndWidth
        self.consWnd.dockTop().dockRight()
        self.consWnd.menu.refresh()
        self.consWnd.menu.autoSize()
        self.consWnd.refresh()
        self.consWnd.autoSize()
        self.consWnd.width = self.consWndWidth
        #self.consWnd.height = self.consWnd.layout.height
        self.moneyWnd.refresh()
        self.moneyWnd.autoSize()
        self.moneyWnd.width = self.consWnd.width
        self.moneyWnd.dockBottom().dockRight()

    def show(self):
        TIME = 35
        self.refresh()

        t = Transition()

        t.addChild(self.consWnd,
            startRect=(self.consWnd.left, -self.consWnd.bottom),
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
            self.consWnd,
            endRect=(ika.Video.xres + self.consWnd.width, self.consWnd.top),
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
        self.consWnd.draw()
        self.moneyWnd.draw()

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

            result = self.consWnd.menu.update()
            
            self.consWnd.refresh()
            
            if result is None:
                continue
            elif result is Cancel:
                self.hide()
                return
            elif result != len(self.item.dormant):
                price = self.consWnd.item.price
                for a in self.consWnd.menu.adding:
                    price += a.price
                if self.consWnd.item.dormant[result] in self.consWnd.menu.adding:
                    self.consWnd.menu.adding.remove(self.consWnd.item.dormant[result])
                elif self.consWnd.item.dormant[result].price + price <= engine.player.stats.money:
                    self.consWnd.menu.adding.append(self.consWnd.item.dormant[result])
                self.consWnd.menu.createContents()
                self.refresh()
            else:
                newItem = item.Item(self.item.name)
                newItem.dormant = self.item.dormant[:]
                for a in self.consWnd.menu.adding:
                    newItem.attribs.append(a)
                    newItem.dormant.remove(a)
                engine.player.stats.money -= newItem.totalPrice
                self.hide()
                return newItem

        assert False, 'Execution should never reach this point.'
        
class ShopWindow(gui.Frame):

    def __init__(self, *args, **kw):
        super(ShopWindow, self).__init__(*args, **kw)
        self.layout = self.createLayout()
        self.addChild(self.layout)

    def createLayout(self):
        return layout.VerticalBoxLayout()
        
    def refresh(self):
        #stats = engine.player.stats
        self.layout.setChildren(self.createContents())
        self.layout.layout()
        
        
class ItemWindow(IconTableWindow):
    
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
            
            price = self.item.totalPrice
            
            if price <= engine.player.stats.money:
                yellow = "#[FF00FFFF]"
                white = "#[FFFFFFFF]"
                red = "#[FFAAAAFF]"
                blue = "#[FFFFAAAA]"
                gold = "#[FFAAFFFF]"
                green = "#[FFAAFFAA]"
            else:
                yellow = white = red = blue = gold = green = "#[FFAAAAAA]"
                
            attribsLabel = gui.ColumnedTextLabel(columns=3, pad=10)
            attribsLabel.addText('%sBase' % red, "%s..." % white, "%s%i" % (gold, self.item.price))
            [attribsLabel.addText('%s%s' % (blue, `a`), "%s..." % white, "%s%i" % (white, a.price)) for a in self.item.attribs]
            attribsLabel.addText('%sTotal' % gold, "%s..." % gold, "%s%i" % (gold, price))
            attribsLabel.autoSize()
            
            dormantLabel = gui.ColumnedTextLabel(columns=3, pad=10)
            
            if self.item.dormant:
                [dormantLabel.addText('%s%s' % (green, `a`), "%s..." % green, "%s%i" % (green, a.price)) for a in self.item.dormant]
            else:
                dormantLabel.addText('None', '', '')
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
    
class ItemConsWindow(ShopWindow):

    def __init__(self, *args, **kw):
        super(ItemConsWindow, self).__init__(*args, **kw)
        self.item = None
        self.menu = None
    
    def createContents(self):
        
        if self.item:
            
            price = self.item.totalPrice
            for p in self.menu.adding:
                price += p.price
        
            yellow = "#[FF00FFFF]"
            white = "#[FFFFFFFF]"
            red = "#[FFAAAAFF]"
            blue = "#[FFFFAAAA]"
            gold = "#[FFAAFFFF]"
            green = "#[FFAAFFAA]"
                
            attribsLabel = gui.ColumnedTextLabel(columns=3, pad=10)
            attribsLabel.addText('%sBase' % red, "%s..." % white, "%s%i" % (gold, self.item.price))
            [attribsLabel.addText('%s%s' % (blue, `a`), "%s..." % white, "%s%i" % (white, a.price)) for a in self.item.attribs]
            [attribsLabel.addText('%s%s' % (blue, `a`), "%s..." % white, "%s%i" % (white, a.price)) for a in self.menu.adding]
            attribsLabel.addText('%sTotal' % gold, "%s..." % gold, "%s%i" % (gold, price))
            attribsLabel.autoSize()
            
            return [ gui.StaticText(text='%s%s' % (yellow, self.item.name)),
                     gui.StaticText(text=''),
                     attribsLabel,
                     gui.StaticText(text=''),
                     gui.StaticText(text='%sDormant Attributes:' % green),
                     self.menu,
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
        self.amount = engine.player.stats.money
        self.text.y += 2
    
class DormantMenuWindow(Menu):

    def __init__(self):
        super(DormantMenuWindow, self).__init__(textctrl=gui.ColumnedTextLabel(columns=3, pad=10))
        self.item = None
        self.adding = []
    
    def refresh(self):
        self.createContents()
        
    def createContents(self):
        
        self.clear()
        
        if self.item:
            
            green = "#[FFAAFFAA]"
            blue = "#[FFFFAAAA]"
            gray = "#[FFAAAAAA]"
            
            if self.item.dormant:
                price = self.item.totalPrice
                for a in self.adding:
                    price += a.price
                for a in self.item.dormant:
                    if a in self.adding:
                        col = blue
                    elif a.price + price > engine.player.stats.money:
                        col = gray
                    else:
                        col = green
                    self.addText('%s%s' % (col, `a`), "%s..." % col, "%s%i" % (col, a.price))
        
        self.addText('Buy','','')