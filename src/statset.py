class StatSet(object):

    STAT_NAMES = (
        '_hp', '_mp', 'maxhp', 'maxmp', 'att', 'mag', 'pres', 'mres', 'level',
        'exp', 'next',
        'money',
        'speed',
    )

    def __init__(self, **kw):
        for name in self.STAT_NAMES:
            setattr(self, name, kw.get(name, 0))
        # special hack:
        if 'hp' in kw:
            self.hp = kw['hp']
        if 'mp' in kw:
            self.mp = kw['mp']

        # Speed defaults to 100, not 0 :P
        self.speed = kw.get('speed', 100)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise KeyError, key

    def __setHp(self, value):
        self._hp = max(0, min(self.maxhp, value))

    def __setMp(self, value):
        self._mp = max(0, min(self.maxmp, value))

    hp = property(
        fget=lambda self: self._hp,
        fset=__setHp
    )

    mp = property(
        fget=lambda self: self._mp,
        fset=__setMp
    )

    def clone(self):
        s = StatSet()
        for name in self.STAT_NAMES:
            setattr(s, name, getattr(self, name))
        return s
