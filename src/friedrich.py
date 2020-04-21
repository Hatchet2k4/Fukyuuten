import ika
import engine
from xi import textbox
from entity import Entity

from npc import Npc
import animator

_friedAnim = {
    'fly': ((
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        animator.makeAnim((2, 3), 20),
        ), True)
}

class Friedrich(Npc):
    SPRITE = 'friedrich.ika-sprite'

    def __init__(self, ent):
        super(Friedrich, self).__init__(ent, _friedAnim)
        anim = 'fly'

