from mapscript import *
import textbox
import dir
from fish import Fish
from friedrich import Friedrich

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 96)))


def firstConvo():
    if 'firstconvo' not in engine.saveData:
        stone = ika.Entity(110, 60, 1, 'artifact.ika-sprite')

        fish = Fish(ika.Entity(110, 60, 2, 'fish.ika-sprite'))
        fish.ent.mapobs = fish.ent.entobs = fish.ent.isobs = False
        fish.ent.speed = 200
        engine.addEntity(fish)

        fried = Friedrich(ika.Entity(176, 60, 1, 'friedrich.ika-sprite'))
        fried.ent.speed = 120
        fried.ent.mapobs = fried.ent.entobs = fried.ent.isobs = False
        fried.anim = 'fly'
        engine.addEntity(fried)

        engine.player.stop()
        engine.saveData['firstconvo'] = True
        engine.beginCutScene()
        ana = engine.player.ent
        ana.specframe = 0

        engine.synchTime()
        text("left", "anastasia3", "Pfft!  I can't believe I came away empty handed today!  If it wasn't for that flock of gulls I'd still have that seventy-pounder.")
        delay(33)
        ana.specframe = 24
        text("left", "anastasia3", "You hear me?!  Give me back my fish!")

        fish.x, fish.y, fish.layer = (110, 60, ana.layer + 1)
        fish.move(dir.DOWN, 120)

        tick()
        while fish.isMoving():
            tick()
            draw()

        engine.things.append(Quake(10))
        ana.specframe = 23
        text(ana, "anastasia2", "Ouch!!!")
        delay(80)

        fried.x, fried.y = 176, 60
        fried.move(dir.DOWN, 70)
        delay(1)
        while fried.isMoving(): delay(1)

        text((180, 100), "Drop something?")
        delay(100)
        text(ana, '...')
        delay(50)
        text(ana, 'mmph.')
        ana.specframe = 1

        fish.move(dir.DOWN, 32)
        fried.move(dir.DOWN, 70)

        delay(1)
        while fried.isMoving(): delay(1)

        ana.specframe = 3
        text("left", "anastasia", "Friedrich!  It's been almost a week!")
        text("right", "friedrich", "Indeed!  It has been quite some time.  Oh, but I've got some stories for you!")
        text("left", "anastasia", "Yeah?  Find any new treasure on that deserted isle?")
        text("right", "friedrich", "You wouldn't believe me if I told you.  I shall have to take you there someday.  We'll plan a trip!")
        text("left", "anastasia", "Ooooh!  Sounds like fun!")
        text("right", "friedrich", "As a matter of fact, there is something I'd like to show you at my shop.  Swing by when you get a chance.")
        text("left", "anastasia", "Sure!  I need to get this fish down to the village anyway.")
        text("right", "friedrich", "Oh do take your time, dear.")

        engine.destroyEntity(fish)
        fried.move(dir.UP, 160)
        fried.anim = 'fly'

        tick()
        while fried.isMoving():
            tick()
            draw()

        engine.destroyEntity(fried)
        engine.endCutScene()
        engine.synchTime()



toGreen01 = exitTo('green_01.ika-map', 5, 25, 1)
