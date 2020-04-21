import ika
import sound
import data

    
class Attribute(object):
    '''Attribute baseclass.
    '''

    def __init__(self, string):
        super(Attribute, self).__init__()
        self.value, self.price = self.parse(string)
    
    def apply(self, player):
        pass
    
    def deapply(self, player):
        pass

    def parse(self, string):
        tokens = string.split(' ')
        tokens.remove('for')
        return tokens[0], int(tokens[1])
        

class StatModifier(Attribute):
    
    realStatNames = {
        'Max HP': 'maxhp',
        'Attack': 'att',
        'Magic': 'mag',
        'Defense': 'pres',
        'Resistance': 'mres',
        }

    def apply(self, player):
        if self.value.isdigit():
            player.stats.__dict__[self.realStatNames[self.statName]] += int(self.value)
        elif self.value.contains('%'):
            pass
    
    def deapply(self, player):
        if self.value.isdigit():
            player.stats.__dict__[self.realStatNames[self.statName]] -= int(self.value)
        elif self.value.contains('%'):
            pass            
    
    def __repr__(self):
        if not self.value:
            return '%s Same' % self.statName
        elif self.value < 0:
            return '%s -%s' % (self.statName, self.value)
        else:
            return '%s +%s' % (self.statName, self.value)
    
class HPModifier(StatModifier):
    statName = 'Max HP'

class AttackModifier(StatModifier):
    statName = 'Attack'

class MagicModifier(StatModifier):
    statName = 'Magic'
    
class DefenseModifier(StatModifier):
    statName = 'Defense'
    
class ResistanceModifier(StatModifier):
    statName = 'Resistance'

attributeTypes = {
    'maxhp' : HPModifier,
    'att' : AttackModifier,
    'mag' : MagicModifier,
    'pres' : DefenseModifier,
    'mres' : ResistanceModifier,
    }