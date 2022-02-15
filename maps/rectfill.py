import ikamap as ika
#import noisetoolgreen
import random

X1 = Y1 = X2 = Y2 = -1
   

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


def OnMouseDown(x, y):
    global buttonDown, X1, Y1
    X1, Y1 = ika.Editor.MapToTile(x, y)


def OnMouseUp(x, y):
    global buttonDown, X1, Y1, X2, Y2
    X2, Y2 = ika.Editor.MapToTile(x, y)

    for x in range(min(X1, X2), max(X1, X2) + 1):
        for y in range(min(Y1, Y2), max(Y1, Y2) + 1):
            ika.Map.SetTile(x, y, ika.Editor.curlayer, RandomTile(ika.Editor.curtile))            



