import ika
import engine
from thing import Thing


class NullSound(object):
    def __init__(self):
        self.position = 0
        self.volume = 1.0

    def Play(self):
        pass

    def Pause(self):
        pass


null = NullSound()


class Sound(NullSound):
    'temp'

    def __init__(self, fname):
        pass

    def Play(self):
        pass

# sound effects ---------------------------------------------------------------------

# TOOLS (BATTLE)
sword1, sword2, sword3 = [ika.Sound('sounds/sword%i.ogg' % i) for i in range(1,4)]
spear1, spear2, spear3 = [ika.Sound('sounds/spear%i.ogg' % i) for i in range(1,4)]
spearCharged = ika.Sound('sounds/spear2.ogg')
spearCharged.pitchshift = 1.125 #range from 0.5 to 2.0, default 1.0
grapple1, grapple2 = [ika.Sound('sounds/grapple%i.ogg' % i) for i in range(1,3)]

# HIT (BATTLE)
playerHit = ika.Sound('sounds/playerhit.ogg')
enemyHit = ika.Sound('sounds/enemyhit.ogg')
sporeHit = ika.Sound('sounds/sporehit.ogg')
maneaterHit = ika.Sound('sounds/maneaterhit.ogg')

# DIE (BATTLE)
playerDie = ika.Sound('sounds/playerdie.ogg')
enemyDie = ika.Sound('sounds/enemydie.ogg')
maneaterDie = ika.Sound('sounds/maneaterdie.ogg')

# MONSTER (BATTLE)
maneaterHead = ika.Sound('sounds/maneaterhead.ogg')
maneaterTentacle = ika.Sound('sounds/maneatertentacle.ogg')
tentacleStrike = null

# OTHER (BATTLE)
deflect = ika.Sound('sounds/deflect.ogg')
fall = ika.Sound('sounds/fall.ogg')

# OTHER (FIELD)
switch = ika.Sound('sounds/switch.ogg')
powerup = ika.Sound('sounds/powerup.ogg')
dooropen = ika.Sound('sounds/dooropen.ogg')
doorclose = ika.Sound('sounds/doorclose.ogg')
itempickup = ika.Sound('music/victory.ogg')

# UI (FIELD)
newGame = ika.Sound('sounds/newgame.ogg')
menuMove = cursorMove = ika.Sound('sounds/menumov.ogg')
menuSelect = ika.Sound('sounds/menusel.ogg')


# LOOPS (N/A)
earthquake = ika.Music('sounds/earthquake.ogg')
earthquake.loop = True


# music -----------------------------------------------------------------------
# all music.  Never ever let go. (because I'm lazy)

music = {}
music['silence'] = NullSound()
music['title'] = ika.Music('music/title.ogg')
music['island'] = ika.Music('music/island1.ogg')
music['town'] = ika.Music('music/town.ogg')
music['dungeon'] = ika.Music('music/dungeon.ogg')
music['storyscene'] = ika.Music('music/story.ogg')
music['boss'] = ika.Music('music/boss.ogg')
music['victory'] = ika.Music('music/victory.ogg')
music['victory'].loop = False   

class Crossfader(Thing): #important Music handler!
    def __init__(self):
        self.oldMusic = []
        self._music = None
        self.inc = 0.01
        self.tempmusic = None
        self._update = self.playnormal
        self.limit = 0
        
    def _setMusic(self, value):
        assert value is not None
        self._music = value

    music = property(lambda self: self._music, _setMusic)

    def pause(self):
        self.music.Pause()
        
    def resume(self):
        self.music.Play()

    def playandresume(self, newMusic, timelimit): #plays a song then resumes the original
        self.pause()
        self.tempmusic = newMusic
        self.tempmusic.position=0
        
        self.tempmusic.Play()
        self.limit=timelimit
        self._update = self.playtemp

    def reset(self, newMusic):
        if newMusic is self.music:
            return
        if newMusic in self.oldMusic:
            self.oldMusic.remove(newMusic)
        if self.music is not None:
            if self.music not in self.oldMusic:
                self.oldMusic.append(self.music)
            self.music = newMusic
            self.music.volume = 0.0
            self.music.loop = True
            self.music.Play()
        else:
            self.music = newMusic
            self.music.volume = 1.0
            self.music.loop = True
            self.music.Play()
        print str(self.oldMusic) + " - " +str(len(self.oldMusic))
        
        
            

    def kill(self):
        if self.music:
            self.music.volume = 0.0
            self.music.Pause()
            self._music = None
            for m in self.oldMusic:
                m.volume = 0
            self.oldMusic = []


    #update functions
    def playnormal(self):
        i = 0
        while i < len(self.oldMusic):
            m = self.oldMusic[i]
            m.volume -= self.inc
            if m.volume <= 0:
                m.Pause()
                self.oldMusic.pop(i)
            else:
                i += 1
        self.music.volume += self.inc
        if self.music.volume>1.0: self.music.volume=1.0
        if not self.oldMusic and self.music.volume >= 1.0:
            return True
    
    def playtemp(self):
        if self.tempmusic.position>=self.limit:
            self.tempmusic.Pause()
            self.tempmusic = None
            self.resume()
            self._update = self.playnormal        

    def update(self):
        self._update() #can be playnormal or playtemp

    def draw(self):        
        #engine.font.Print(15, 5, "Main Volume: "+str(self.music.volume))
        #for i, m in enumerate(self.oldMusic):
        #    engine.font.Print(15, 15+10*i, "OldMusic Volume: "+str(m.volume))
        pass
        

fader = Crossfader()

def playMusic(fname):
    if fname in music:
        m = music[fname]
    else:
        m = ika.Music(fname)
        m.loop = True
        music[fname] = m            
    fader.reset(m)
    if fader not in engine.things:
        engine.things.append(fader)

def killMusic():
    fader.kill()
