"""
A simple ikamapMap tool for painting random tiles.

It's pretty sucky right now, though, because
I'm too lazy to look up a random number generating
function.
"""

import ikamap
import random

#tiles now can handle many groups of tiles!

# green.vsp

tiles = [

       [ #group 1, stone tiles
        ( 8, 12),
        ( 9, 14),
        (16, 12),
        (17, 12),
        (24, 12),
        (25, 14),
        (32, 12),
        (33, 12),        
    ], [ #group 2, dark grass
        ( 1, 84),
        ( 2,  8),
        ( 3,  8),
    ], [ #group 3, grass
        ( 4, 84),
        ( 5,  8),
        ( 6,  8),
    ], [ #group 4, random decorations (layer 2)
        ( 0, 80),
        ( 7,  5),
        (77,  5),
        (78,  5),
        (79,  5),
    ]
    
]


buttonDown = False
oldX = -1
oldY = -1


def RandomTile(t):
   global tiles

   for group in tiles:
      for a in group:
         if a[0] == t: #tile is in the range
            return ChooseTile(group)

   return t


def ChooseTile(tilegroup):
   weight = random.randint(0, 100)
   for tile in tilegroup:
      if weight < tile[1]:
         return tile[0]
      weight -= tile[1]

   return tilegroup[0][0]


def Draw(x, y):
    global oldX, oldY

    x, y = ikamap.Editor.MapToTile(x, y)

    if x == oldX and y == oldY:
        return
    oldX, oldY = x, y

    ikamap.Map.SetTile(x, y, ikamap.Editor.curlayer, RandomTile(ikamap.Editor.curtile))


def OnMouseDown(x, y):
    global buttonDown
    buttonDown = True
    Draw(x, y)


def OnMouseMove(x, y):
    if buttonDown:
        Draw(x, y)


def OnMouseUp(x, y):
    global buttonDown, oldX, oldY
    buttonDown = False
    oldX = -1
    oldY = -1
