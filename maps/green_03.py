
from mapscript import *

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    playMusic('town')
    if engine.player:
        engine.player.stats.hp = engine.player.stats.maxhp

    if 'rescued' not in engine.saveData:
        del ika.Map.entities["friedrich"]
        


def friedrich():
    fried = ika.Map.entities["friedrich"]
    ana = engine.player.ent

    engine.beginCutScene()


    text(fried, "friedrich2", "What are you doing here? You should be looking for the source of the earthquakes?")
    text(ana, "anastasia", "Just stocking up on some supplies.")
    text(fried, "friedrich", "Ok. But don't take too long, there could be another one soon!")


    engine.endCutScene()


def dancer():
    dancertext()


def dancer2():
    dancertext()


def dancertext():
    d1 = ika.Map.entities["dancer"]
    d2 = ika.Map.entities["dancer2"]
    ana = engine.player.ent

    engine.beginCutScene()

    firstTime = 'dancerconvo' not in engine.saveData
    secondTime = 'dancerconvo2' not in engine.saveData
    
    engine.saveData['dancerconvo'] = True

    if 'rescued' not in engine.saveData:
        
        if firstTime:
            engine.saveData['dancerconvo'] = True
            text(ana, "anastasia", "Have you seen Friedrich?")
            text(d1, "dancer1", "Oh yes!  The little wolf bird!")
            text(d2, "dancer2", "He's so cuuute!")
            text(d1, "dancer1", "Oh I know!  I just want to cuddle him and squeeze him until he..")
            text(ana, "anastasia3", "*ahem*")
    
        text(d1, "dancer1", "...um...I think I saw him running after a goblin.")
        text(d2, "dancer2", "Yeah...to the north.")
    
        if firstTime:
            text(d1, "dancer1", "He accused that little goblin of stealing something from him.  Personally, I think goblins are harmless.")
            text(d2, "dancer2", "They're just so cute!")
            text(d1, "dancer1", "I know!  I could just eat them right up!")
            ana.specframe = 3
            text(ana, "anastasia2", "(You would...)")
            
    elif not secondTime:
        engine.saveData['dancerconvo2'] = True
        text(d1, "dancer1", "Oooh, Friedrich is back!  I'm so glad!")

    else:
        text(d2, "dancer2", "I'm getting kinda tired...")

    engine.endCutScene()


def guy2():
    me = ika.Map.entities['guy2']

    if 'rescued' not in engine.saveData:
        text(me, "Oh hello. Have you seen Friedrich? He's not home.")
        text(engine.player, "anastasia", "No, I thought he would be here. I'll keep looking.")
    else:
        text(me, "What a beautiful pot.")


def guy3():
    me = ika.Map.entities['guy3']
    text(me, '...')
    
    if 'guy3convo' not in engine.saveData:
        engine.saveData['guy3convo'] = True
        text(engine.player, "anastasia3", "My, aren't we talkative.")


def woman():
    me = ika.Map.entities['woman']
    text(me, "What a beautiful day!")


def yolander():
    yo = ika.Map.entities["yolander"]
    ana = engine.player.ent

    if 'fishconvo' not in engine.saveData and 'rescued' not in engine.saveData:
        engine.saveData['fishconvo'] = True

        text(yo, "yolander", "Oh my!  That's the biggest catch you've made all month!")
        text(ana, "anastasia3", "Yeah...  Except it's the only one I have.")
        text(yo, "yolander", "Tsk tsk, Anastasia!  How can I run a restaurant without fish?")
        text(ana, "anastasia", "I'm really sorry, Yolander.  This really hasn't been my day.  I swear, those gulls were out to get me!")
        text(yo, "yolander", "Sure, sure.  Don't worry about it.  This should be enough for today.  Here you are..")

        engine.player.stats.money += 20
        text(ana, "Recieved 20 shells!")
        text(yo, "yolander", "Don't spend it all in one place!")

    elif 'rescued' not in engine.saveData:
        text(yo, "yolander", "Have you found Friedrich yet? I haven't seen him all day..")
        text(engine.player, "anastasia", "No, not yet. Maybe I'll try looking north.")
        
    else:
        text(yo, "yolander", "So when are you gonna catch some more fish for your favorite customer?")
        text(engine.player, "anastasia", "Um... soon, but first I have some business to take care of.")
        text(yo, "yolander", "Okay, but just make sure none of my customers starve. I have a business to run too!")



toGreen02 = exitTo('green_02.ika-map', 3, 3, 43)
