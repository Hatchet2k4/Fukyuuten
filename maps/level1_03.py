from mapscript import *
import sound
import engine
import ika

toTemple01 = exitTo('level1_01.ika-map', 29, 9, 3)
toTemple04 = exitTo('level1_04.ika-map', 52, 32, 26)

def AutoExec():
    if 'level1_door1' in engine.saveData:        
        removeDoor()

def keyDoor():
    if 'level1_key1' in engine.saveData and 'level1_door1' not in engine.saveData:
        engine.saveData['level1_door1'] = 'True'
        sound.dooropen.Play()
        removeDoor()
        
def removeDoor():
    l = ika.Map.FindLayerByName('B2')
    ika.Map.SetTile(52, 3, l, 0)
    ika.Map.SetTile(52, 2, l, 0)
    ika.Map.SetObs(52, 3, l, 0)
    
    
