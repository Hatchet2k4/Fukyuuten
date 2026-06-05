import ika
import os

def Map2TMX(mapName, tilesetName):
        
    ika.Log('Saving map ' + mapName)
    ika.Map.Switch(mapName)
    
    twidth = theight = 16
    
    mheight = ika.Map.height / theight
    mwidth = ika.Map.width / twidth
    

    s = '''<?xml version="1.0" encoding="UTF-8"?>\n
<map version="1.10" tiledversion="1.12.2" orientation="orthogonal" renderorder="right-down" compressionlevel="0" width="''' + str(mwidth) + '''" height="''' + str(mheight) + '''" tilewidth="''' +str(twidth) + '''" tileheight="''' + str(theight) +   '''" infinite="0" nextlayerid="''' + str(ika.Map.layercount + 1) + '''" nextobjectid="1">
<tileset firstgid="1" source="''' + tilesetName + '''"/> '''
    
    for l in range(ika.Map.layercount):                
        n, w,h, wrapx,wrapy = ika.Map.GetLayerProperties(l)
        lwidth = w 
        lheight = h 
        
        s += '''\n<layer id="''' +str(l + 1) + '''" name="'''  + n + '''" width="''' +  str(lwidth) + '''" height="''' + str(lheight) +  '''"> 
        <data encoding="csv">
'''          
        
        
        for y in range(mheight):
            for x in range(mwidth):            
                t=ika.Map.GetTile(x,y,l)
                if t>0: t+=1 #Tile ID's seem to be off by 1 in the TSX tileset, using this to correct. 
                s+= str(t) + ','
                
        s = s[:-1] #hack to remove the last comma from the list
        s+='\n</data></layer>'
    s+='\n</map>'
    
    file(mapName + '.tmx', 'wt').write(s)                    
    #canvas.Save('map2img/' +  mapName + '.png')
                    
        
     
    
    
def SaveAllMaps():
    savemaps=[]
    #tiles=self.rip_tiles('tiles.png', 16, 16, 6, 503)
    
    #hack!
    ika.Log('SaveAllMaps')
    try:
        raw_names = os.listdir('maps')
        savemaps = []
        for f in raw_names:
            if f.endswith('ika-map') and f.startswith('green') and not f.startswith('green_05'):
                savemaps.append('maps/'+f)
        
        ika.Log( str(savemaps) )
    except: 
        
        ika.Log('Error')
        return None

    ika.Log('maps: ' + str(savemaps))
    
    for m in savemaps:
        #self.Map2Img(m, tiles)    
        Map2TMX(m, 'green.tsx')