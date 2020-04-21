import ika
import config
import controls
import engine
import effects
import gui

#------------------------------------------------------------------------------

def WrapText(text, maxWidth, font):
    """Wraps the text to the given pixel width, using the font
       specified.  Returns a list of strings.
    """
    result = []
    pos = 0
    lastSpace = 0
    while len(text):
        # find a space, tab, or newline.  whichever comes first.
        # if the word can be appended to the current line, append it.
        # if not, and the current line is not empty, put it on a new line.
        # if the word is longer than a single line, hack it wherever, and make the hunk its own line.
        # find the next space, tab, or newline.
        if pos >= len(text):    # hit the end of the string?
            result.append(text) # we're done.  add the last of it to the list
            break               # and break out
        if text[pos].isspace():
            lastSpace = pos
            if text[pos] == '\n':      # Newline.  Chop.
                result.append(text[:pos])
                text = text[pos + 1:]
                pos = 0
                lastSpace = 0
                continue
        l = font.StringWidth(text[:pos])
        if l >= maxWidth:        # Too wide.  Go back to the last whitespace character, and chop.
            if lastSpace > 0:
                result.append(text[:lastSpace])
                text = text[lastSpace + 1:]
                pos = 0
                lastSpace = 0
            else:                       # No last space!  Hack right here, since the word is obviously too long.
                result.append(text[:pos])
                text = text[pos + 1:]
            continue
        pos += 1
    return result

#------------------------------------------------------------------------------

controls.init()

class Tinter(object):

    def __init__(self):
        self.curTint = 0
        self.tint = 0
        self.time = 0

    def draw(self):
        self.curTint += self.curTint < self.tint
        self.curTint -= self.curTint > self.tint
        if self.curTint:
            ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                               ika.RGB(0, 0, 0, self.curTint), True)

tint = Tinter()
crap = [tint]  # things to draw along with the map

def draw():
    ika.Map.Render()
    for c in crap:
        c.draw()

#------------------------------------------------------------------------------

def textBox(where, txt):
    # where is either a point or an entity
    WIDTH = 200
    width = WIDTH
    text = WrapText(txt, width, engine.font)
    width = max([engine.font.StringWidth(s) for s in text])
    height = len(text) * engine.font.height
    if isinstance(where, ika.Entity):
        ent = where
        x, y = ent.x + ent.hotwidth / 2 - ika.Map.xwin, ent.y - ika.Map.ywin
    else:
        x, y = where
    if x < ika.Video.xres / 2:
        x -= width / 2
    width = WIDTH
    if x + width + 16 > ika.Video.xres:
        text = WrapText(txt, ika.Video.xres - x - 16, engine.font)
        width = max([engine.font.StringWidth(s) for s in text])
        height = len(text) * engine.font.height
    frame = gui.ScrollableTextFrame()
    frame.addText(*text)
    frame.autoSize()
    if y > ika.Video.yres / 2:
        y += 32
    else:
        y -= frame.Height + 16
    frame.Position = x, y
    return frame

#------------------------------------------------------------------------------

def text(where, txt):
    """Displays a text frame.
       Where txt can be either a point or an ika entity.
    """
    frame = textBox(where, txt)
    while not controls.attack():
        draw()
        frame.draw()
        ika.Video.ShowPage()
        ika.Input.Update()

#------------------------------------------------------------------------------

def animate(ent, frames, delay, thing=None, loop=True, text=None):
    class AnimException(Exception):
        pass
    # frames should be a list of (frame, delay) pairs.
    if thing is not None:
        crap.append(thing)
    if text is not None:
        text = textBox(ent, text)
        crap.append(text)
    try:
        while True:
            for frame in frames:
                ent.specframe = frame
                d = delay
                while d > 0:
                    d -= 1
                    draw()
                    ika.Video.ShowPage()
                    ika.Delay(1)
                    ika.Input.Update()
                    if controls.attack():
                        loop = False
                        raise AnimException
            if not loop:
                raise AnimException
    except:  #except what?
        if thing:
            crap.remove(thing)
        if text:
            crap.remove(text)
        ent.specframe = 0

#------------------------------------------------------------------------------
# Scene code
#------------------------------------------------------------------------------

_scenes = {}


# TODO: transitions
def scene(name):
    global grandpa, kid1, kid2, kid3
    savedPos = [(e.x, e.y) for e in engine.entities]
    # hide 'em all
    for e in engine.entities:
        e.x, e.y = -100, -100
    ika.Map.Switch('%s/cabinmap.ika-map' % config.MAP_PATH)
    grandpa = ika.Map.entities['grandpa']
    kid1 = ika.Map.entities['kid1']
    kid2 = ika.Map.entities['kid2']
    kid3 = ika.Map.entities['kid3']
    effects.fadeIn(100)
    _scenes[name]()
    engine.saveData['name'] = 'True'
    effects.fadeOut(100)
    grandpa = kid1 = kid2 = kid3 = None
    # FIXME? AutoExec will be called when you do this!
    if engine.mapName:
        ika.Map.Switch('maps/' + engine.mapName)
        for e, pos in zip(engine.entities, savedPos):
            e.x, e.y = pos


# name : function pairs
def addScene(function):
    _scenes[function.__name__] = function

#------------------------------------------------------------------------------
# Ear's (disgusting) functions
#------------------------------------------------------------------------------

PAUSE = 0
SPEAKING = 1
NOD = 2
TALKING = ([PAUSE] * 3 +
           [SPEAKING] * 2 +
           [PAUSE] * 3 +
           [SPEAKING] * 2 +
           [PAUSE] * 3 +
           [NOD])
speech = text
narration = lambda t: animate(grandpa, TALKING, 25, text=t)

#------------------------------------------------------------------------------
# Scenes
#------------------------------------------------------------------------------

def fake_scene_1():
    speech(grandpa, "Listen kids, for in my drunken stupour, I shall tell a "
                    "tale like none you've ever heard!")
    speech(grandpa, '*hic*')
    speech(kid1, 'All right!  Alchohol induced ranting!')
    speech(kid2, 'COCKS!')
    speech(kid3, 'POTTYMOUTH!')
    speech(kid2, 'You just shut the fuck up, freak!')
    speech(kid3, ':(')
    speech(grandpa, 'And thus, the world exploded.')


def fake_intro():
    speech(grandpa, 'Heeeeey kids!')
    speech(grandpa, "Sit back, fuckers, 'cause I'm gonna tell you a story, and"
                    "you're going enjoy it whether you want to or not.")
    speech(kid1, '. . .')
    speech(kid2, 'Who are you, and what are you doing in our house?')
    animate(kid3, (0, 1), delay=20, text="PLEASE DON'T RAPE ME!")
    animate(grandpa, (6, 0, 7, 0), delay=100, text='The curse compels me to '
            'rant about shit you do not care about to atone for my previous '
            'child molestations.')
    speech(kid2, 'HURRAY, STORY TIME!')
    speech(kid1, 'Tell us a story about ramming your old, wrinkly--')
    speech(grandpa, 'It was a dark and stormy night!')
    speech(grandpa, 'Perfect for a night on the town.')
    speech(grandpa, 'Except that, as a child molester, I had to live far away '
                    'from town.')
    speech(kid3, 'OMG.')
    speech(grandpa, 'So, anyway, there I was in the middle of nowhere, off to'
                    'town so I could find somewhere cozy to hide my '
                    'cock. . . .')


def intro():
    speech(kid1, 'Tell us a story!')
    animate(kid2, (1,), delay=10, text='Yeah, the one about the ice man!')
    animate(kid3, (0, 1), delay=20, text="Yeah!!")
    speech(grandpa, "Isn't that story a little scary?")
    speech(kid1, 'No!')
    speech(kid2, 'Please tell us!')
    speech(grandpa, 'Oh all right.  Ahem.')
    animate(kid3, (0, 1), delay=20, text="I'm scared!!")
    tint.tint = 200
    narration("Across the frozen hills of Kuladriat, hunters pursued a man"
              "like any other prey.  Northward their prey ran until, at the"
              "foot of Mount Durinar, an icy chasm confronted him.")
    narration("The crack of a bow sounded across the vale; an instant later"
              "its arrow burying itself in the leg of the hunted man.  His leg"
              "buckled beneath him, and he tumbled down the cold ravine--")
    narration("--the sound of stone 'gainst stone resounding.")
    tint.tint = 0
    narration("A sharp whistle signified the hunt's end.  The hunters would"
              "not bother to claim their prize, for it was far too cold: his"
              "fate had come.")


def impasse():
    narration("The stone walls seemed to draw in closer, choking the very "
              "breath from him: the way was sealed.  However, though despair "
              "welled within him, a glint of hope shone through the gelid "
              "rock.  If only there were some way to breach it . . .")


def nearend():
    tint.tint = 200
    narration("As he neared his journey's end, he grew tired, and cold, and "
              "hungry.")
    narration("He was willing to do anything to make such neverending misery "
              "cease, once and for all.")
    narration("He considered . . . going back from whence he came, then.")
    narration("But, if he were to do so, he would then have to face the same "
              "same trials which had taken such a weary toll on his spirit to "
              "begin with.")
    tint.tint = 0
    speech(kid1, 'Did he go back?')
    speech(kid2, 'Yeah!')
    speech(kid3, "No way!  He's way too brave!  Yeah!")
    narration("In the end, no one knows whether he attempted to return . . . "
              "all that is important is the outcome.""")
    narration("But should he have gone back, he would have found the greatest "
              "reward of all.  Not peace . . . and not relief . . . but "
              "courage.  The courage to continue again.")

#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

addScene(intro)
#addScene(rune_of_water)
#addScene(rune_of_fire)
#addScene(rune_of_wind)
#addScene(impasse)
addScene(nearend)
#addScene(forebattle)
#addScene(epilogue)
