from mapscript import *

def AutoExec():
    playMusic('dungeon')

def spirit():
    ana = engine.player
    spirit = ika.Map.entities['spirit']

    text(spirit, "spirit",      "So it is you who has answered my call.  Wait...a woman?")
    text(ana, 'anastasia3',     "Hey!  What's that supposed to mean?")
    text(spirit, "spirit",      "Erm...nothing!  Tell me...how did you do it?")
    text(ana, 'anastasia',      "That plant thing?  I er.... poked it with a sharp piece of metal, you see.")
    text(ana, 'anastasia',      "Most anything eventually stops moving if you poke enough holes in it.")
    text(spirit, "spirit",      "The guardian you defeated was the very reason I called you here.  He finally broke free of the spell put on him a millennium ago.  ")
    text(spirit, "spirit",      "It seems he tampered with the crystal.")
    text(ana, 'anastasia',      "Crystal?  What's this thing for, anyway?")
    text(spirit, "spirit",      "Are your people truly so blind?  Did you not read the great Book of Kojima??")
    text(ana, 'anastasia3',     "Um... 'book'?  Is that a kind of plant?")
    text(spirit, "spirit",      "Ana, this crystal is what keeps this island afloat.  You see, thousands of years ago...")
    text(spirit, "spirit",      "blah blah blah, and a big flood, blah blah blah.  The earth was blah and covered in water.  It was up to us Kojima to blah blah blah.  Blah blah blah blah blah blah.")
    text(spirit, "spirit",      "And that's how Green Island got here!  It is all a part of Fukyuuten!")
    text(ana, 'anastasia',      "Cool!  So...um.  What am I supposed to do now?")
    text(spirit, "spirit",      "The crystal's power is fading.  If you don't find a replacement soon, this whole island could fall into the ocean!")
    text(ana, 'anastasia2',     "Oh no!  Where can I get a new one!")
    text(spirit, "spirit",      "On the desert island that wasn't built!")
    text(ana, 'anastasia2',     "???")
    text(spirit, "spirit",      "Yes!  As hard as Your Mother worked these past few weeks, they didn't haul sufficient deriere to get a second island completed. ")
    text(spirit, "spirit",      "So, you'll have to settle for this text ending!")

    delay(100)
    ika.Exit('*AND THUS THE ISLAND WAS DOOMED.  EVERYBODY DIED GRUESOME, HORRIBLE DEATHS.  THANK YOU FOR PLAYING*')

toTemple15 = exitTo('level1_15.ika-map', 9, 9, 16, 'y')
