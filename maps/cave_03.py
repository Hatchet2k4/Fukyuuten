from mapscript import *
from friedrich import Friedrich
import sound

def toggleBlocks():
    for y in range(4, 9):
        ika.Map.SetTile(10, y, 1, 0)
        ika.Map.SetObs(10, y, 1, False)


def AutoExec():
    #if 'rescued' in engine.saveData:
    #    del ika.Map.entities['friedrich']
    pass #

def friedrich():


    fried = engine.entFromEnt[ika.Map.entities['friedrich']]

    if 'rescued' not in engine.saveData:
        engine.saveData['rescued'] = True



        ana = engine.player.ent
        engine.beginCutScene()

        sound.playMusic('storyscene')
        text(fried, "friedrich2", "Ana!  Thank goodness!")
        text(ana, "anastasia3", "What happened to you?")
        fried.specframe = 5
        text(fried, "friedrich", "Remember the item I told you about earlier? One of the little buggers took it! ")
        fried.specframe = 4
        text(fried, "friedrich", " I thought nothing of chasing down a young goblin...but then he came in here.")
        text(ana, "anastasia", "A cave full of goblins!")
        text(fried, "friedrich2", "Yes...how they built a home this close to town without anyone noticing still eludes me.")
        text(fried, "friedrich", "But it wasn't all bad. We have the item back. Look!")
        fried.specframe = 1
        text(ana, "anastasia", "What is that? It's...")
        text(fried, "friedrich", "Yes..")
        text(ana, "anastasia2", "...just a rock!")

        fried.specframe = 7
        text(fried, "friedrich2", "Just a rock??  Do you have any idea how old it is?")
        text(ana, "anastasia", "A thousand years?")
        text(fried, "friedrich2", "ONLY A THOUSA...oh...well, you're right, actually.  It is precisely 998 years old.")
        text(ana, "anastasia2", "How do you know?")
        fried.specframe = 4
        text(fried, "friedrich", "Because it belongs to the Kojima...a race of people who once populated this very island. ")
        text(fried, "friedrich", "They were wiped out by a natural disaster ages ago.")


        text(fried, "friedrich", "It's amazing, really.  This is perhaps the oldest Kojima artifact ever found!")

        text(ana, "anastasia2", "Ooooh!  So that means this is really, really important!")
        fried.specframe = 7
        text(fried, "friedrich2", "YES!!!")
        text(ana, "anastasia", " Wow, Fred...this could make you filthy rich!")
        fried.specframe = 4
        text(fried, "friedrich", "Let's not get ahead of ourselves.  I still have many authenticity tests to run.  ")
        text(fried, "friedrich", "You never know who might be out to prank us.")
        text(ana, "anastasia3", "Don't worry...if anybody tries that I'll kick their butts!")


        engine.things.append(Quake(20))
        t = ika.GetTime()
        while ika.GetTime() < t + 10: delay(1)

        text(ana, "anastasia2", "What the...")
        text(fried, "friedrich", "Hmm?")
        text(ana, "anastasia2", "Didn't you feel the ground shaking??")
        text(fried, "friedrich", "Well, as you can tell, I don't do a lot of standing around...")

        engine.things.append(Quake(100, x=4, y=4))
        t = ika.GetTime()
        while ika.GetTime() < t + 200: delay(1)
        fried.specframe = 6
        text(fried, "friedrich2", "Sweet Candy!  What was THAT?")
        text(ana, "anastasia2", "Look! The artifact is glowing!")

        fried.specframe = 4
        text(fried, "friedrich", "Hmm...")
        text(ana, "anastasia", "What do you think it could mean?")
        text(fried, "friedrich", ".It seems that...hmm...")
        text(fried, "friedrich2", "...that the shaking and the glowing MUST be related!")
        text(ana, "anastasia3", "JESUS, Fred!  Even I could've figured that one out!  You know, you're not as smart as you look.")
        text(fried, "friedrich", "Hmph!  I...honestly have no idea what it could be!")
        text(ana, "anastasia3", "Arg!!")
        fried.specframe = 5
        text(fried, "friedrich2", "Unless... there could be one posibility. ")
        text(fried, "friedrich", "But...of course it is all a Kojima legend.  But it couldn't possibly...")
        text(ana, "anastasia", "What's the legend?")
        text(fried, "friedrich", 'Well...it is believed that the natural disaster that caused the Kojima to vanish was this very thing. ')
        text(fried, "friedrich", 'It was called an "earthquake."')

        text(ana, "anastasia", "Earthquake?")
        text(fried, "friedrich", "Yes.  But it's all impossible of course.  Earthquakes are a myth.")

        fried.specframe = 6
        engine.things.append(Quake(100, x=2, y=2))
        t = ika.GetTime()
        while ika.GetTime() < t + 100: delay(1)


        text(ana, "anastasia3", "That feel like a myth to you?!?")
        text(fried, "friedrich2", "Aaaagh!")
        text(ana, "anastasia2", "Wait...I think it's trying to tell me something.  These arrows...what are they?")
        fried.specframe = 4
        text(fried, "friedrich", "They look like directions!  Everytime the stone lights up it's pointing you in a direction.")
        text(ana, "anastasia", "It's pointing...west! What's to the west?")
        text(fried, "friedrich", "I don't know...maybe you should see!")
        text(ana, "anastasia3", "Me?  You're the one with wings, buster!  Why do I have to run my ass off?")
        text(fried, "friedrich2", "Dear, Anastasia.  I can't carry that heavy artifact in my talons!  It would be suicide!")
        text(ana, "anastasia3", "Oh I get it...you're still scared of the tiny little itsy-bitsy goblins.")
        text(fried, "friedrich", "No!  I just...don't want to drop it is all.  Now, head west, Ana!")
        text(ana, "anastasia", "Right!")
        text(fried, "friedrich", "Good luck!")
        text(ana, "anastasia3", "...What a wimp")
        engine.endCutScene()
        sound.playMusic('dungeon')
    else:
        text(fried, "friedrich", "Good luck!")

toCave02 = exitTo('cave_02.ika-map', 13, 31, 4)
