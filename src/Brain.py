import ika


class Brain(object):
    """The brain is a very high level abstraction over an enemy's
       behavior.  Brains consist of a number of moods, each of which
       having its own desirability factor (an arbitrary integer.)

       A mood is checked every so often.  For now, it's random, weighted
       by desirability.
    """

    def __init__(self):
        super(Brain, self).__init__()
        self.moods = []
        self.curMood = None

    def chooseMood(self):
        """Weighted random pick."""
        n = ika.Random(0, sum([x.desirability for x in self.moods]))
        for p in self.moods:
            if n <= p.desirability:
                return p
            n -= p.desirability

    def think(self):
        self.curMood = self.chooseMood()
        return self.curMood

# moods -----------------------------------------------------------------------

class Mood(object):

    def __init__(self, desirability):
        self.desirability = desirability


class Flee(Mood):
    pass


class Attack(Mood):
    pass


class Passive(Mood):
    pass


class Regroup(Mood):
    pass
