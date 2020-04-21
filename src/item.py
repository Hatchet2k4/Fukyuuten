import ika
import sound
import data
from attribute import attributeTypes


class Item(object):
    '''Item baseclass.
    '''

    def __init__(self, name):
        super(Item, self).__init__()
        
        self.name = name
        
        attributes = data.itemData[name]
        self.type = attributes.get('type', 'useless')
        self.desc = attributes.get('desc', 'No description available.')
        self.overlaySprite = attributes.get('overlay', 'overlay_spear1.ika-sprite')
        self.overlay = ika.Entity(0, 0, 0, self.overlaySprite)
        self.icon = data.itemIcons[name]
        
        attribs = attributes.get('attribs', {})
        dormant = attributes.get('dormant', {})
        
        self.attribs = [attributeTypes[k](v) for k,v in attribs.items()]
        self.dormant = [attributeTypes[k](v) for k,v in dormant.items()]
        
        self.price = int(attributes.get('price', 0))
        
        if self.overlay:
            self.overlay.isobs = self.overlay.entobs = self.overlay.mapobs = False
        
    def applyAll(self, player):
        for a in self.attribs:
            a.apply(player)
            
    def deapplyAll(self, player):
        for a in self.attribs:
            a.deapply(player)
        
    totalPrice = property(lambda self: self.price + sum([a.price for a in self.attribs]))