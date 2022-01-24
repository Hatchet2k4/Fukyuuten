from mapscript import *
import sound

def AutoExec():
    engine.background = ika.Image('gfx/sky_bg.png')
    engine.mapThings.append(Clouds('gfx/sky_shadows.png', tint=ika.RGB(255, 255, 255, 128)))
    engine.mapThings.append(Clouds('gfx/sky_clouds.png', tint=ika.RGB(255, 255, 255, 128)))    
    #playMusic('town')
    if engine.player:
        engine.player.stats.hp = engine.player.stats.maxhp

    if 'rescued' not in engine.saveData:
        del ika.Map.entities["friedrich"]

def innkeeper():
    me = ika.Map.entities['innkeeper']
    text('right', "I'll be running an inn... soon!")
        

def guard1():
    me = ika.Map.entities['guard1']
    ana = engine.player.ent    
    if 'guardconvo' not in engine.saveData:
        text('right', "Hey Anastasia. It's a tough job, but someone's gotta keep the goblins out!")
        text('left', "anastasia", "I'm just glad it's not me. I found enough of them just walking here!")
        text('right', "There's certainly been more of them lately.")
        engine.saveData['guardconvo'] = True
    else:
        text('right', "Don't worry, the goblins no better than to try and attack our town!")
        
    
def guard2():
    me = ika.Map.entities['guard2']
    text('right', "Welcome to Haven! ...")
    
    text(me, "This armor is too hot...")
    
def friedrich():
    fried = ika.Map.entities["friedrich"]
    ana = engine.player.ent

    if 'lookingForSource' not in engine.saveData:
        engine.beginCutScene()
        text('right', "friedrich2", "What are you doing here? You should be looking for the source of the earthquakes?")
        text('left', "anastasia", "I'm just stocking up on some supplies.")
        text('right', "friedrich", "Ok. But don't take too long, there could be another one soon!")
        engine.saveData['lookingForSource'] = True
    else:
        text('right', "friedrich", "Still need supplies?")

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
            text('left', "anastasia", "Have you seen Friedrich?")
            text('right', "dancer1", "Oh yes!  The little wolf bird!")
            text('right', "dancer2", "He's so cuuute!")
            text('right', "dancer1", "Oh I know!  I just want to cuddle him and squeeze him until he..")
            text('left', "anastasia3", "*ahem*")
    
        text('right', "dancer1", "...um...I think I saw him running after a goblin.")
        text('right', "dancer2", "Yeah...to the north.")
    
        if firstTime:
            text('right', "dancer1", "He accused that little goblin of stealing something from him.  Personally, I think goblins are harmless.")
            text('right', "dancer2", "They're just so cute!")
            text('right', "dancer1", "I know!  I could just eat them right up!")
            ana.specframe = 3
            text('left', "anastasia2", "(You would...)")
            
    elif not secondTime:
        engine.saveData['dancerconvo2'] = True
        text(d1, "dancer1", "Oooh, Friedrich is back!  I'm so glad!")

    else:
        text(d2, "dancer2", "I'm getting kinda tired...")

    engine.endCutScene()


def guy2():
    me = ika.Map.entities['guy2']

    if 'rescued' not in engine.saveData:
        text('right', "Oh hello. Have you seen Friedrich? He's not home.")
        text('left', "anastasia", "No, I thought he would be here. I'll keep looking.")
    else:
        text('right', "What a beautiful pot.")


def guy3():
    me = ika.Map.entities['guy3']
    text(me, '...')
    
    if 'guy3convo' not in engine.saveData:
        engine.saveData['guy3convo'] = True
        text('left', "anastasia3", "My, aren't we talkative.")


def woman():
    me = ika.Map.entities['woman']
    text(me, "What a beautiful day!")


def yolander():
    yo = ika.Map.entities["yolander"]
    ana = engine.player.ent

    if 'fishconvo' not in engine.saveData and 'rescued' not in engine.saveData:
        engine.saveData['fishconvo'] = True
        text('left', "anastasia", "Hey Yolander! Here's my fish for today.")
        text('right', "yolander", "Oh my! That's the biggest catch you've made all month!")
        text('left', "anastasia3", "Yeah... Except it's the only one I have.")
        text('right', "yolander", "Tsk tsk, Anastasia! How can I run my restaurant without fish?")
        text('left', "anastasia", "I'm really sorry, Yolander. This really hasn't been my day. I swear, those gulls were out to get me!")
        text('right', "yolander", "Oh don't worry about it, this should be enough for today. Here you are..")
        sound.powerup.Play()
        engine.player.stats.money += 20
        text('left', "Recieved 20 shells!")
        text('right', "yolander", "Don't spend it all in one place!")
        if 'friedMissing' in engine.saveData:
            text('left', "anastasia", "Uh huh.. by the way, have you seen Friedrich?")
            text('right', "yolander", "Hmm, no, not since he went to visit you when he saw you return from fishing.")    
            text('left', "anastasia", "Well I'm sure he's around somewhere...")    

    elif 'rescued' not in engine.saveData:
        text('right', "yolander", "Have you found Friedrich yet? I haven't seen him all day..")
        text('left', "anastasia", "No, not yet. Maybe I'll try looking north.")
        
    else:
        text('right', "yolander", "So when are you gonna catch some more fish for your favorite customer?")
        text('left', "anastasia", "Um... soon, but first I have some business to take care of.")
        text('right', "yolander", "Okay, but just make sure none of my customers starve. I have a business to run too!")

def friedMissing():
    if 'friedMissing' not in engine.saveData and 'rescued' not in engine.saveData and 'dancerconvo' not in engine.saveData:  
        engine.saveData['friedMissing'] = True
        text('left', "anastasia", "Hmm, Friedrich isn't here. I wonder where he went.")


toGreen02 = exitTo('green_02.ika-map', 3, 3, 43)
