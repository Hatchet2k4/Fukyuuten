from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(128, 160, 128, 96)))

def smith():
    me = ika.Map.entities['smith']
    text(me, 'smith', 'Hello! I can make you weapons... but... now!')
    s = ShopScreen()
    s.addItem('Arrowhead Spear', 'Sharp Slicer', 'Divine Lance', 'Valiance', 'Hades Hand', 'Soul Spike')
    s.run()
    #text(me, 'smith', '(Come back in a later version)')

toGreen04 = exitTo('green_04.ika-map', 18, 18, 1)
