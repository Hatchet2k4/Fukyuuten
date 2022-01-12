'''Town NPCs
'''

import ika
import engine
import animator
from entity import Entity

from npc import Npc

class TownPerson(Npc):
    SPRITES = (
        'townguy2.ika-sprite',
        'townguy3.ika-sprite',
        'townwoman.ika-sprite',
        'guard.ika-sprite',
        'townwoman2.ika-sprite',
        'yolander.ika-sprite',
        'smith.ika-sprite',
        'fish.ika-sprite',
        'nothing.ika-sprite',
    )


class Dancer(Npc):
    SPRITE = 'towndancer.ika-sprite'
    SPRITE2 = 'towndancer2.ika-sprite'

    _anim = {
        'dance': ((
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            animator.makeAnim((0, 1), 20),
            ),
            True)
    }

    def __init__(self, ent):
        super(Dancer, self).__init__(ent, self._anim)
        self.anim = 'dance'


class Friedrich(Npc):
    SPRITE = 'friedrich.ika-sprite'

    _anim = {
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

    def __init__(self, ent):
        super(Friedrich, self).__init__(ent, self._anim)
        anim = 'fly'

