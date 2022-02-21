from mapscript import *
import dir
from fish import Fish
from friedrich import Friedrich
import ika
import sound
from caption import Caption
import engine



def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.bgThings.append(Clouds('gfx/sky_clouds.png', speed=(0.1, 0.025), tint=ika.RGB(255, 255, 255, 220)))           
    engine.mapThings.append(ClippedClouds('stencils/green_00.ika-map.png', 'gfx/sky_shadows.png', tint=ika.RGB(255, 5, 5, 255)))        
    
    if 'firstconvo' in engine.saveData:
        engine.things.append(Caption("Anastasia's House", font=engine.font2))

def firstConvo():
    #if 'firstconvo' not in engine.saveData:    
    if False:    
        xwin = ika.Map.xwin
        ywin = ika.Map.ywin
    
        stone = ika.Entity(110, 60, 1, 'artifact.ika-sprite')

        fish = Fish(ika.Entity(110, 60, 2, 'fish.ika-sprite'))
        fish.ent.mapobs = fish.ent.entobs = fish.ent.isobs = False
        fish.ent.speed = 300
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

        sound.fall.Play()
        delay(75)
        fish.x, fish.y, fish.layer = (110, -20, ana.layer + 1)
        fish.move(dir.DOWN, 200)
        
        tick()
        while fish.isMoving():
            tick()
            draw()

        engine.things.append(Quake(20))
        ana.specframe = 23
        
        apos=(ana.x, ana.y+16-ywin)
        
        text(apos, "anastasia2", "left", "Ouch!!!")
        delay(80)

        fried.x, fried.y = 176, 60
        fried.move(dir.DOWN, 70)
        delay(1)
        
        
        
        while fried.isMoving(): delay(1)

        fpos=(160, fried.y+24-ywin)

        text(fpos, "Dropped something?")
        delay(100)
        text((ana.x-8, ana.y+24-ywin), '...')
        delay(50)
        text((ana.x-8, ana.y+24-ywin), 'Mmph..')
        ana.specframe = 1

        fish.move(dir.DOWN, 32)
        fried.move(dir.DOWN, 70)

        delay(1)
        while fried.isMoving(): delay(1)

        ana.specframe = 3
        text("left", "anastasia3", "That thing is heavy.. ")
        text("left", "anastasia", "Oh, Friedrich! Did you scare that fish out of the gulls? It's good to see you, it's been almost a week!")
        text("right", "friedrich", "Indeed! It has been quite some time.  Oh, but I've got some stories for you!")
        text("left", "anastasia", "Yeah? Did you find any new treasure on that deserted island?")
        text("right", "friedrich", "It was a very enlightening experience. I shall have to take you there someday.  We'll plan a trip!")
        text("left", "anastasia", "Ooooh! Sounds like fun!")
        text("right", "friedrich", "As a matter of fact, there is something I found that I'd like to show you at my shop. Swing by when you get a chance.")
        text("left", "anastasia", "Sure! I need to get this fish down to Yolander anyway.")
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
        engine.things.append(Caption("Anastasia's House", font=engine.font2))


timer = 0

def AnaHouse():
    global timer
    if timer == 0:
        result = textMenu("left","anastasia","Should I take a rest?", options=["Yes", "No"] )
        timer = 100
    else:
        timer -=1
    
    


toGreen01 = exitTo('green_01.ika-map', 5, 25, 1)
