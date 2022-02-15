"""
A simple ikaMap tool for painting random tiles.

It's pretty sucky right now, though, because
I'm too lazy to look up a random number generating
function.
"""

import ika

buttonDown = False
oldX = -1
oldY = -1




def Draw():
    layer = ika.Editor.curlayer            
    w, h = ika.Map.GetLayerSize(layer)     
    i=0
    for y in range(h):
        for x in range(w):
            ika.Map.SetTile(x, y, ika.Editor.curlayer, i)
            i+=1


def OnMouseDown(x, y):
    global buttonDown
    if not buttonDown: 
        Draw()
    buttonDown = True
    



def OnMouseUp(x, y):
    global buttonDown
    buttonDown = False
    
