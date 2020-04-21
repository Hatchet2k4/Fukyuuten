import config
from entities import *

# ENEMIES
import bee
import goblin
import plant
# -------------
import bug
import jelly
import frankenhead

# GENERATORS
import hive
# ----------------
import pot


# BOSSES
import maneater

# NPCS AND OTHER
from obstacle import Gap
from savepoint import SavePoint
from townperson import *
from spirit import Spirit

# match each sprite name up with the associated class
spawnMap = {

    bee.Bee.SPRITE : bee.createBee,
    goblin.Goblin.SPRITE : goblin.createGoblin,
    goblin.UberGoblin.SPRITE : goblin.createUberGoblin,
    goblin.DesertGoblin.SPRITE : goblin.createDesertGoblin,
    plant.Plant.SPRITE : plant.createPlant,
        
    bug.Bug.SPRITE : bug.createBug,
    jelly.Jelly.SPRITE : jelly.createJelly,
    frankenhead.Frankenhead.SPRITE : frankenhead.createFrankenhead,
    
    # -------------------
    
    hive.Hive.SPRITE : hive.createHive,
        
    pot.Pot.SPRITE : pot.createPot,

    # -------------------
    
    maneater.Maneater.SPRITE : maneater.Maneater,

    # -------------------

    SavePoint.SPRITE : SavePoint,

    Gap.SPRITE: Gap,
    Gap.SPRITE2: Gap,
    Gap.SPRITE3: Gap,

    Dancer.SPRITE : Dancer,
    Dancer.SPRITE2 : Dancer,
    Friedrich.SPRITE : Friedrich,

    Spirit.SPRITE : Spirit
}


for p in TownPerson.SPRITES:
    spawnMap[p] = TownPerson


class SpawnException(Exception):
    pass


def createEntity(spriteName, *args, **kw):
    assert (isinstance(spriteName, basestring),
            "createEntity: spriteName must be a string, not '%r'" %
            type(spriteName))
    if spriteName not in spawnMap:
        raise SpawnException("Don't know how to create entity '%s'" %
                             spriteName)
    factory = spawnMap[spriteName]
    return factory(*args, **kw)
