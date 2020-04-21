import ika
import config
import engine
import sound
from clouds import Clouds


_text = """\
FUKYUU TEN
ETERNAL SKIES
***




MAIN PROGRAM
-
Andy Friesen


ENEMY SCRIPTING
-
Andy Friesen
Troy Potts


STORY SCRIPTING
-
Francis Brazeau


ARTWORK
-
Corey Annis


MUSIC
-
Troupe Gammage


MAPS
Corey Annis
Fancis Brazeau
Andy Friesen
Troy Potts


STORYLINE
-
Corey Annis
Andy Friesen


***


Hey look, we did another one of these.
Good golly, but they're fun to make.

... I got nothing.  Maybe I can get someone
else to add something.
-- Andy

""".split('\n')


def credits():
    m = sound.music.get('title',
                        ika.Music('%s/title.ogg' % config.MUSIC_PATH))

    m.loop = True
    sound.fader.kill()
    sound.fader.reset(m)
    bg = ika.Image('%s/sky_bg.png' % config.IMAGE_PATH)
    clouds = Clouds('%s/sky_clouds.png' % config.IMAGE_PATH, tint=ika.RGB(255, 255, 255, 128), speed=(0.1, 0.05))
    y = -ika.Video.yres
    font = engine.font  # stupid
    def draw():
        ika.Video.Blit(bg, 0, 0, ika.Opaque)
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                           ika.RGB(0, 0, 0, 128), True)
        firstLine = int(y) / font.height
        adjust = int(y) % font.height
        length = (ika.Video.yres / font.height) + 1
        print firstLine
        Y = -adjust
        while Y < ika.Video.yres and firstLine < len(_text):
            if firstLine >= 0:
                font.CenterPrint(160, Y, _text[firstLine])
            Y += font.height
            firstLine += 1
        ika.Video.DrawTriangle((0, 0, ika.RGB(0, 0, 0)),
                               (ika.Video.xres, 0, ika.RGB(0, 0, 0, 0)),
                               (0, 60, ika.RGB(0, 0, 0, 0)))
        ika.Video.DrawTriangle((ika.Video.xres, ika.Video.yres,
                                ika.RGB(0, 0, 0)),
                               (0, ika.Video.yres, ika.RGB(0, 0, 0, 0)),
                               (ika.Video.xres, ika.Video.yres - 60,
                                ika.RGB(0, 0, 0, 0)))
        clouds.draw()
    now = ika.GetTime()
    while True:
        t = ika.GetTime()
        delta = (t - now) / 10.0
        y += delta
        now = t
        clouds.update()
        draw()
        ika.Video.ShowPage()
        ika.Input.Update()
