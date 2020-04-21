'''

'''

import ika

from xi.effects import fade, fadeIn, fadeOut

def grabScreen():
    return ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

def crossFade(time, startImage=None, endImage=None):
    """Crossfades!  Set either startImage or endImage, or both."""
    assert startImage or endImage
    if not startImage:
        startImage = grabScreen()
    if not endImage:
        endImage = grabScreen()

    endTime = ika.GetTime() + time
    now = ika.GetTime()

    while now < endTime:
        opacity = (endTime - now) * 255 / time
        ika.Video.ClearScreen()
        ika.Video.Blit(endImage, 0, 0)
        ika.Video.TintBlit(startImage, 0, 0, ika.RGB(255, 255, 255, opacity))
        ika.Video.ShowPage()
        ika.Input.Update()
        now = ika.GetTime()
