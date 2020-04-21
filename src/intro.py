import ika
import config
import controls
import subscreen
import sound
import effects
from engine import font
from clouds import Clouds

clouds = Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 128))

class _DoneException(Exception):
    pass


def clearScreen(col=ika.RGB(0, 0, 0)):
    ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres, col, True)


def delay(draw, count):
    scr = effects.grabScreen()
    draw()
    effects.crossFade(30, scr)

    while count > 0:
        draw()
        ika.Delay(1)
        count -= 1
        ika.Video.ShowPage()
        ika.Input.Update()
        if controls.attack1():
            raise _DoneException()

    draw()


def intro():
    ikalogo = ika.Image('%s/ika.png' % config.IMAGE_PATH)
    gbabg = ika.Image('%s/sky_bg.png' % config.IMAGE_PATH)
    gba = ika.Image('%s/gba.png' % config.IMAGE_PATH)
    yourmom = ika.Image('%s/yourmother.png' % config.IMAGE_PATH)
    isabitch = ika.Image('%s/yourmother2.png' % config.IMAGE_PATH)
    controls.attack1() # unpress
    v = ika.Video
    d = 40

    def stub():
        clearScreen()
        
    def showGba():
        gbabg.Blit(0,0)
        v.Blit(gba, (v.xres - gba.width) / 2, (v.yres - gba.height) / 2)
        clouds.update()
        clouds.draw()

    try:
        delay(stub, 10)
        delay(showGba, 440)
        delay(lambda: v.Blit(ikalogo, 0, 0, ika.Opaque), 440)
        delay(lambda: v.Blit(yourmom, 0, 0, ika.Opaque), 450)
        delay(lambda: v.Blit(isabitch, 0, 0, ika.Opaque), 1)
    except _DoneException:
        return


def menu():
    clouds.speed = (1.0, .75)
    bg = ika.Image('%s/title_bg.png' % config.IMAGE_PATH)
    logo = ika.Image('%s/title_logo.png' % config.IMAGE_PATH)
    cursor = ika.Image('%s/ui/pointer.png' % config.IMAGE_PATH)
    result = None
    cursorPos = 0
    menuTop = 175
    menuLeft = 120
    secrat = 0
    menuItems = ("New Game", "Load Game", "Quit Game")
    wnd = subscreen.Window('gfx/ui/win_%s.png')
    FADE_TIME = 60
    opacity = 0
    opacity2 = 0
    opacity3 = 0

    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        clouds.update()
        clouds.draw()        
        font.Print(2, 2, "v.1/05")

        ika.Video.TintBlit(logo, 0, 0, ika.RGB(255,255,255, opacity))

        wnd.draw(menuLeft - 5, menuTop - 5, ika.Video.xres - (menuLeft * 2), (len(menuItems) * font.height) + 10, ika.RGB(255,255,255,opacity3))
        y = 0
        for i in menuItems:
          font.Print(menuLeft, menuTop + y, '#[%02XFFFFFF]%s' % (opacity2, i))
          y += font.height
        ika.Video.TintBlit(cursor, menuLeft - cursor.width - 2, menuTop + cursorPos * font.height + 2, ika.RGB(255,255,255,opacity2))

    for i in range(FADE_TIME - 1, -1, -1):
        draw()
        ika.Video.DrawRect(
            0, 0, ika.Video.xres, ika.Video.yres,
            ika.RGB(255, 255, 255, i * 255 / FADE_TIME), True
        )
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)

    u = 0  # unpress hack
    while result == None:
        opacity = min(255, opacity + 2)
        opacity2 = min(255, opacity2 + (opacity>=128)*2)
        opacity3 = min(255, opacity2*3)
        draw()
        ika.Video.ShowPage()
        ika.Input.Update()
        ika.Delay(1)
        if opacity2 == 255:
            if controls.up.pressed:
                sound.menuMove.Play()
                if cursorPos > 0:
                    cursorPos -= 1
                else:
                    secrat += 1
                    if (secrat == 6):
                        menuItems = ("New Game", "Load Game", "Quit Game", "New Game +")
                        cursorPos = 3
    
            elif controls.down.pressed and cursorPos < (len(menuItems) - 1):
                sound.menuMove.Play()
                cursorPos += 1
            elif controls.attack1():
                result = cursorPos

    if result == 0:
        sound.newGame.Play()
    else:
        sound.menuSelect.Play()
    return result
