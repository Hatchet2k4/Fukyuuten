from mapscript import *
from friedrich import Friedrich
import dir

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')    
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 96)))        
    if 'temple01_revealed' in engine.saveData:
        clearWater()
    

def clearWater():
    ika.Map.SetLayerTint(ika.Map.FindLayerByName("Secret"), ika.RGB(255,255,255,0))
    ika.Map.SetObs(25, 11, 1, 0)
    ika.Map.SetObs(26, 11, 1, 0)

def friedTotem():
    
    if 'temple01_revealed' not in engine.saveData:

        if numEnemies() > 0:
            engine.player.stop()
            engine.beginCutScene()
            text((10, 10), "friedrich2", "No WAY am I going down there until you take care of the rest of those pests!")
            engine.endCutScene()
            
        else:
            engine.saveData['temple01_revealed'] = True
            engine.player.stop()
            fried = Friedrich(ika.Entity(48, 0, 1, 'friedrich.ika-sprite'))
            fried.ent.speed = 120
            fried.ent.mapobs = fried.ent.entobs = fried.ent.isobs = False
            fried.anim = 'fly'
            engine.addEntity(fried)

            ana = engine.player.ent
            ana.specframe = 1

            engine.beginCutScene()

            #do quaky lake revealing things!
            layer = ika.Map.FindLayerByName("Secret")
            x, y = ika.Map.GetLayerPosition(layer)
            length = 500
            engine.things.append(Quake(length))
            i = 0
            while i < length:
                i+=1
                if i > length/2: #start fading when it's halfway done
                    ika.Map.SetLayerTint(layer, ika.RGB(255,255,255,255-int(i*1.0/(length/2) * 255)))
                y+=0.2
                ika.Map.SetLayerPosition(layer, x, int(y))
                delay(1)
            clearWater()

            engine.endCutScene()


toGreen07 = exitTo('green_07.ika-map', 12, 12, 1, 'y')
toGreen09 = exitTo('green_09.ika-map', 25, 25, 28)
toTemple01 = exitTo('level1_01.ika-map', 11, 9, 13)

