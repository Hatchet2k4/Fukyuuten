import engine
from statset import StatSet


class SaveGame(object):

    def __init__(self, fileName=None):
        self.stats = StatSet()
        self.flags = {}
        self.mapName = ''
        self.pos = (0, 0, 0)
        if fileName is not None:
            self.load(fileName)

    def getStats(self):
        self.stats = engine.player.stats.clone()

    def getFlags(self):
        self.flags = {}
        for k, v in engine.saveData.iteritems():
            if isinstance(v, (int, basestring, list, tuple)):
                self.flags[k] = v

    def setStats(self):
        engine.player.stats = self.stats.clone()

    def setFlags(self):
        engine.saveData.clear()
        for k, v in self.flags.iteritems():
            engine.saveData[k] = v


    @staticmethod
    def currentGame():
        s = SaveGame()
        s.getStats()
        s.getFlags()
        s.mapName = engine.mapName
        if s.mapName.startswith('maps'): s.mapName = s.mapName[5:]
        p = engine.player
        s.pos = (p.x, p.y, p.layer)
        return s

    def setCurrent(self):
        self.setStats()
        self.setFlags()

    def save(self, fileName):
        file(fileName, 'wt').write(str(self))

    def load(self, fileName):
        self.read(file(fileName, 'rt'))

    def __str__(self):
        s = ''
        for k in StatSet.STAT_NAMES:
            s += '%s=%i\n' % (k, getattr(self.stats, k))
        s += 'FLAGS\n'
        s += "MAPNAME='%s'\n" % self.mapName
        s += "POS='%s'\n" % ','.join([str(x) for x in self.pos])
        for var, val in engine.saveData.iteritems():
            if not var.startswith('_'):
                if isinstance(val, (int, str)):
                    s += '%s=%r\n' % (var, val)
                elif isinstance(val, (list, tuple)):
                    s += '%s=LIST\n' % var
                    for el in val:
                        s += '  %s\n' % el
                    s += 'END\n'
        return s

    def read(self, f):
        lines = [x.strip() for x in f.readlines()]

        def parse(v):
            v = v.strip()
            if v == 'LIST':
                l = []
                while True:
                    v = lines.pop(0)
                    if v == 'END':
                        break
                    else:
                        l.append(parse(v))
                return l
            elif v.startswith("'"):
                return v[1:-1]
            elif v in ('True', 'False'):
                return bool(v)
            else:
                return int(v)

        # Read stats
        while True:
            s = lines.pop(0)
            if s == 'FLAGS':
                break
            p = s.find('=')
            k, v = s[:p], s[p + 1:]
            setattr(self.stats, k, parse(v))
        # read flags
        while lines:
            s = lines.pop(0)
            p = s.find('=')
            k, v = s[:p], parse(s[p + 1:])
            if k == 'MAPNAME':
                self.mapName = v
            elif k == 'POS':
                self.pos = tuple([int(x) for x in v.split(',')])
            else:
                self.flags[k] = v

        print self.flags

def test():
    engine.saveData.test1 = 'string'
    engine.saveData.test8 = 1337
    engine.saveData.test1337 = range(10, 40)
    sg = SaveGame.currentGame()
    bleh = SaveGame()
    bleh.load('test.txt')
    bleh.setCurrent()
    s = StatSet.STAT_NAMES
    print engine.saveData.test1
    print engine.saveData.test8
    print engine.saveData.test1337
