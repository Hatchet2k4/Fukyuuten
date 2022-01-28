_dir = dir

import ika
import cabin
import config
import controls
import dir
import data
import effects
import saveload
import sound
import subscreen
from camera import Camera
from caption import Caption, DamageCaption
from gameover import EndGameException, GameOverException
from createentity import createEntity, SpawnException
from hud import HPBar, EXPBar, ShellsIndicator
from player import Player
from npc import Npc
from xi.fps import FPSManager


entities = []
killList = []
player = None
background = None
stencil = None

font = ika.Font(config.FONT)
font2 = ika.Font(config.FONT2)


mapName = ''
mapModule = None
curMap = ''

things = []     # Things that are not entities, but still need to be updated and/or drawn
bgThings = []  # same as things, but is cleared every mapSwitch and is drawn under the map
mapThings = []  # same as things, but is cleared every mapSwitch
fields = []     # Like zones, except the same!
entFromEnt = {} # Maps ika Entity objects to our Entity instances
saveData = {}   # Game flags that need to persist throughout the game.

isCutScene = 0 # if greater than zero, entities are not updated

# framerate regulating stuff:
ticksPerFrame = 100.0 / config.FRAME_RATE
nextFrameTime = 0
fps = FPSManager(config.FRAME_RATE)



def rip_tiles(image, width, height, span, tilecount):
    """This is a simple function that takes any image that is formatted
    like a tileset and rips the tiles into a list which is then
    returned.

    image - path of image to rip from
    width/height - width and height of a single tile
    span - how many tiles per row
    tilecount - number of tiles to rip
    """
    tiles = []
    big_image = ika.Canvas(image)
    for i in range(tilecount):
        tile = ika.Canvas(width, height)
        big_image.Blit(tile, -1 - (i % span * (width + 1)),
                       -1 - (i / span * (height + 1)), ika.Opaque)
        #tiles.append(ika.Image(tile))
        tiles.append(tile)
    return tiles        
    
def saveallmaps():
    savemaps=['green_00', 'green_01', 'green_02','green_03']
    """
    try:
        #raw_names = os.listdir('.\\maps')
        
        savemaps = []
        for f in raw_names:
            if f.endswith('ika-map'):
                savemaps.append(f)
        
        ika.Log( str(savemaps) )
    except: 
        #ika.Log(str(e))
        return None
  
    ika.Log('maps: ' + str(savemaps))
    
    #mantiles={'mannux.vsp': rip_tiles('mannuxvsp.png', 16, 16, 10, 1645) }
    
    """
    tiles = rip_tiles('resources/tiles3.png', 16, 16, 8, 8*52)
    for m in savemaps:
        Map2Img(m+'.ika-map', tiles)  

test = False

pixeldict = {
False: ika.RGB(0,0,0,0),
True: ika.RGB(255,255,255,255)
}

black=ika.RGB(0,0,0,0)

def Map2Img(mapName, tileset):        
    ika.Log('Saving map ' + mapName)
    ika.Map.Switch('maps/' + mapName)
    
    canvas = ika.Canvas(ika.Map.width, ika.Map.height) 
     
       
    for y in range(int(ika.Map.height/16)):
        for x in range(int(ika.Map.width/16)):
            for l in range(ika.Map.layercount):
                t=ika.Map.GetTile(x,y,l)
                tileset[t].Blit(canvas, x*16, y*16, ika.Matte)
                
    #canvas.Save('map2img/' +  mapName + '.png')          
    for y in range(ika.Map.height):
        for x in range(ika.Map.width):
            canvas.SetPixel(x,y, pixeldict[ canvas.GetPixel(x,y) == black  ])   
    
    canvas.Save('stencils/' +  mapName + '.png')


def _clear():
    global things, mapThings, bgThings, field, entFromEnt, saveData
    things = []
    mapThings = []
    bgThings = []
    fields = []
    entFromEnt = {}
    saveData = {}


def init(saveGame=None):
    global killList, camera, player, saveData, stencil
    stencil = ika.Canvas(320,240)

    # clean everything
    killList = entities[:]
    clearKillQueue()
    _clear()

    if saveGame is not None:
        saveData.clear()
        saveData.update(saveGame.flags)
        mapSwitch(saveGame.mapName, fade=False)

    else:
        mapSwitch(config.START_MAP, fade=False)

    if not player:
        player = Player()
    addEntity(player)

    if saveData:
        player.x, player.y, player.layer = saveGame.pos
        saveGame.setCurrent()  # set stats, flags

    else:
        player.x, player.y = config.START_POSITION

        player.layer = ika.Map.FindLayerByName(
            ika.Map.GetMetaData()['entityLayer']
        )

    #temp hack
    player.items.append(player.spear.item)
    player.items.append(player.sword.item)

    camera = Camera()
    camera.center()
    addThing(HPBar(), EXPBar(), ShellsIndicator(), camera)


def beginNewGame():
    screen = effects.grabScreen()

    mapSwitch(config.START_MAP, config.START_POSITION, fade=False)
    init()
    saveData['spear'] = True
    #saveData['sword'] = True

    raw_draw()
    effects.crossFade(50, screen)
    #sound.playMusic('island')

    run()


def loadGame():
    import saveloadmenu
    result = saveloadmenu.loadMenu(fadeOut=False)
    if result:
        temp = effects.grabScreen()
        saveData.clear()
        mapSwitch(result.mapName, result.pos, fade=False)
        init(result)
        raw_draw()
        effects.crossFade(50, temp)
        #sound.playMusic('island')
        run()


def happyFunTime():
    mapSwitch(config.START_MAP, config.START_POSITION, fade=False)
    init()
    saveData['spear'] = True
    saveData['sword'] = True
    player.giveXP(5000)
    player.stats.hp = player.stats.maxhp
    player.stats.mp = player.stats.maxmp
    #sound.playMusic('island')

    run()

def mapSwitch(newMapName, dest=None, fade=True):
    global mapName, mapModule, mapThings, bgThings, fields

    fade = False # temp

    if fade:
        draw()
        screen = effects.grabScreen()

    mapName = newMapName

    # all maps load from MAP_PATH
    mapName = '%s/%s' % (config.MAP_PATH, mapName)
    background = None
    mapThings = []
    bgThings = []
    fields = []
    ika.Map.entities.clear()

    # drop the extension, convert slashes to dots, and prepend the maps
    # package ie 'blah/map42.ika-map' becomes 'maps.blah.map42'
    moduleName = mapName[:mapName.rfind('.')].replace('/', '.')
    mapModule = __import__(moduleName, {}, {}, [''])

    ika.Map.Switch(mapName)
    metaData = ika.Map.GetMetaData()
    readZones(mapModule)
    readEnts(mapModule)

    if player:
        player.state = player.defaultState()

    if dest and player:
        if len(dest) == 2:
            player.x, player.y = dest
            player.layer = ika.Map.FindLayerByName(metaData['entityLayer'])
        elif len(dest) == 3:
            player.x, player.y, player.layer = dest
        else:
            raise Exception

        camera.center()

    if 'music' in metaData:        
        sound.playMusic(metaData['music'])

    if fade:
       draw()
       effects.crossFade(50, screen)

    synchTime()

def warp(dest, fade=True):
    if fade:
        draw()
        img = ika.Video.GrabImage(0, 0, ika.Video.xres, ika.Video.yres)

    player.direction = dir.DOWN
    player.state = player.defaultState()
    player.anim = 'stand'
    player.animate()
    player.x, player.y = dest
    camera.center()
    draw()

    if fade:
        effects.crossFade(50, startImage=img)

    synchTime()


def regulateTiming():
    '''TODO: make this not actually draw.
    Make it yield a value that the caller can use to decide how to draw and delay?
    '''
    global nextFrameTime
    skipCount = 0
    nextFrameTime = ika.GetTime() + ticksPerFrame
    while True:
        t = ika.GetTime()
        # if we're ahead, delay
        if t < nextFrameTime:
            ika.Delay(int(nextFrameTime - t))
        # Do some thinking
        yield 'think'
        # if we're behind, and can, skip the frame.  else draw
        if t > nextFrameTime and skipCount < config.MAX_SKIP_COUNT:
            skipCount += 1
        else:
            skipCount = 0
            #draw()
            yield 'draw'
            #ika.Video.ShowPage()
            #ika.Input.Update()

        nextFrameTime += ticksPerFrame


def run():
    global killList
    try:
        while True:
            tick()
            if controls.cancel() or controls.ui_cancel():
                pause()
            draw()

    except GameOverException:
        gameOver()
        killList = entities[:]
        clearKillQueue()
    except EndGameException:
        killList = entities[:]
        clearKillQueue()



def raw_draw():
    if background:
        ika.Video.ScaleBlit(background, 0, 0, ika.Video.xres, ika.Video.yres)
        for t in bgThings:
                t.draw()               
        ika.Map.Render(*range(ika.Map.layercount))        
    else:     
        ika.Map.Render()
             
    for t in mapThings:
        t.draw()
    for t in things:
        t.draw()

    ika.Input.Update()


def draw():
    fps.render(raw_draw)


def tick():
    # We let ika do most of the work concerning entity movement.
    # (in particular, collision detection)
    ika.ProcessEntities()

    if not isCutScene:
        # update entities
        for ent in entities:
            ent.update()

        # check fields
        for f in fields:
            if f.test(player):
                f.fire()
                break  # Is this the right thing?  Maybe all fields under the player should fire.

    else:
        # update NPC entities only
        for ent in entities:
            if isinstance(ent, Npc):
                ent.update()

    clearKillQueue()

    updateThings()


def updateThings():
    '''Update Things.

        For each thing in each thing list, we update.
        If the result is true, we delete the thing, else
        move on.'''

    for thingList in (things, mapThings, bgThings):
        index = 0
        while index < len(thingList):
            result = thingList[index].update()
            if result:
                thingList.pop(index)
            else:
                index += 1


def addEntity(ent):
    assert ent not in entities
    entities.append(ent)
    entFromEnt[ent.ent] = ent


def destroyEntity(ent):
    ent.x = ent.y = -1000
    ent.stop()
    killList.append(ent)

def addField(field):
    assert field not in fields
    fields.append(field)


def destroyField(field):
    fields.remove(field)


def addThing(*thing):
    things.extend(thing)


def destroyThing(thing):
    things.remove(thing)


def readZones(mapModule):
    '''Read all the zones on the map, and create fields.'''
    fields = []
    for layerIndex in range(ika.Map.layercount):
        zones = ika.Map.GetZones(layerIndex)
        for (x, y, w, h, scriptName) in zones:
            script = getattr(mapModule, scriptName)
            addField(Field((x, y, w, h), layerIndex, script))


def readEnts(mapModule):
    '''Grabs all entities from the map, and adds them to the engine.'''
    global killList
    # making a gamble here:
    # assuming all entities except the player are tied to the map
    if player:
        killList = entities[:]
        killList.remove(player)
        clearKillQueue()
    for ent in ika.Map.entities.itervalues():
        try:
            addEntity(createEntity(ent.spritename, ent))
        except SpawnException, exc:
            print "Unable to create entity using '%s'.  Ignoring." % ent.spritename


def clearKillQueue():
    '''It's a bad idea to tweak the entity list in the middle of an
       iteration, so we queue them up, and nuke them here.
    '''
    global killList
    for ent in killList:
        ent.ent.x, ent.ent.y = -100, 0
        ent.ent.Stop()
        del entFromEnt[ent.ent]
        ika.Map.entities.pop(ent, None)
        ent.destroy()
        entities.remove(ent)
    killList = []


def testCollision(ent):
    return entFromEnt.get(ent.ent.DetectCollision())


def synchTime():
    '''Used to keep the engine from thinking it has to catch up
       after executing an event or something.
    '''
    #global nextFrameTime
    #nextFrameTime = ika.GetTime()
    fps.sync()


def gameOver():
    global fields
    c = Caption(
        'G A M E   O V E R', duration=1000000,
        y=(ika.Video.yres - font.height) / 2
    )
    t = 80
    i = 0
    fields = []
    while True:
        i = min(i + 1, t)
        c.update()
        tick()
        raw_draw()
        # darken the screen, draw the game over message:
        ika.Video.DrawRect(0, 0, ika.Video.xres, ika.Video.yres,
                           ika.RGB(0, 0, 0, i * 255 / t), True)
        c.draw()
        ika.Video.ShowPage()
        ika.Delay(4)
        if i == t and (controls.attack1() or controls.joy_attack1() or controls.ui_accept() or controls.ui_cancel()):
            break


def pause():
    draw()
    s = subscreen.PauseScreen()
    s.run()
    synchTime()


def beginCutScene():
    global isCutScene
    isCutScene += 1


def endCutScene():
    global isCutScene
    isCutScene = max(0, isCutScene - 1)


def delay(duration):
    endTime = ika.GetTime() + duration
    while ika.GetTime() < endTime:
        tick()
        draw()

class Field(object):
    '''A field is just a big invisible thing that does something if the
       player walks on to it.  Warp points can be fields, as can plot-
       based zone thingies.
    '''

    def __init__(self, rect, layer, script):
        self.pos = rect[:2]
        self.size = rect[2:]
        self.layer = layer
        self.script = script
        self.rect = rect

    def fire(self):
        self.script()

    def test(self, p):
        if p.layer != self.layer:
            return False
        x, y = self.pos
        w, h = self.size
        if x - p.ent.hotwidth  < p.x < x + w and \
           y - p.ent.hotheight < p.y < y + h:
            return True
        return False



#saveallmaps()
