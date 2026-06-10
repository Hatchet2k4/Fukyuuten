import ika
import sys
import os
import re
import base64
import zlib

def RipTiles(image, width, height, span=None, tilecount=None):
    """This is a simple function that takes any image that is formatted
    like a tileset and rips the tiles into a list which is then
    returned.

    image - image to rip from
    width/height - width and height of a single tile
    span - how many tiles per row
    tilecount - number of tiles to rip
    """
    tiles = []
    big_image = ika.Canvas(image)

    # do some figurin:) ~infey
    if span == None and tilecount == None:
        span = (big_image.width - 1) / (width + 1)
        tilecount = span * ((big_image.height - 1) / (height + 1))

    for i in range(tilecount):
        tile = ika.Canvas(width, height)
        big_image.Blit(tile, -1 - (i % span * (width + 1)),
                       -1 - (i / span * (height + 1)), ika.Opaque)
        tiles.append(ika.Image(tile))
    return tiles



def SaveAllSprites():    
    savesprites=[]
    #tiles=self.rip_tiles('tiles.png', 16, 16, 6, 503)

    
    ika.Log('SaveAllSprites')
    
    raw_names = os.listdir('sprites')
    
    for f in raw_names:
        if f.endswith('ika-sprite'):
            savesprites.append(f)
    
    ika.Log( str(savesprites) )
    
    for s in savesprites:        
        Sprite2TSX('sprites/', s)
        
def Sprite2TSX(folder, sprite):
   
    s=''
    sname = sprite[:-11]
    parsed_data = parse_file_to_dict(folder+sprite)
    
    tile_width = int(parsed_data['ika-sprite']['frames']['dimensions']['width'])
    tile_height = parsed_data['ika-sprite']['frames']['dimensions']['height']
    hotx = parsed_data['ika-sprite']['frames']['hotspot']['x']
    hoty = parsed_data['ika-sprite']['frames']['hotspot']['x']
    hotwidth = parsed_data['ika-sprite']['frames']['hotspot']['width']
    hotheight = parsed_data['ika-sprite']['frames']['hotspot']['height']   
    count = parsed_data['ika-sprite']['frames']['count']
    
    image = ika.Canvas(folder + sname+ '.png')
    columns = (image.width - 1) // (int(tile_width) + 1)
    rows = (image.height - 1) // (int(tile_height) + 1)
    
    s='''<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="''' + sname + '''" tilewidth="''' + tile_width +  '''" tileheight="''' + tile_height +  '''" tilecount="''' + count +  '''" columns="''' + str(columns) +  '''">
 <image source="''' + sname + '_sheet.png' + '''" width="''' + str(tile_width * columns) +  ''' " height="''' + str(tile_height * rows) +  ''' "/>
 <tile id="0">
  <objectgroup>
   <object id="0" name="Hitbox" x="''' + hotx + '''" y="''' + hoty + '''" width="''' + hotwidth + '''" height="''' + hotheight + '''"/>
  </objectgroup>
 </tile>
</tileset>'''

    print(s)

    #tiles = RipTiles(folder + sname+ '.png', int(tile_width), int(tile_height))
    #bigimage = ika.Canvas(int(tile_width)*columns, int(tile_height)*rows)
    #for y in range(rows):
    #    for x in range(columns):
    #        tiles[y*columns + x].Blit(            bigimage,             x*int(tile_width),            int(int(y)*int(tile_height)))
    
    #bigimage.Save(folder+sname+'_sheet.png')

    file(folder + sname + '.tsx', 'wt').write(s)  
    
    


    

def tokenize(text):
    """Tokenizes parentheses, quoted literals, and words."""
    return re.findall(r'\(|\)|\'[^\']*\'|[^\s()]+', text)

def parse_tokens(tokens_iter):
    """Recursively converts tokenized stream into nested lists."""
    result = []
    for token in tokens_iter:
        if token == '(':
            result.append(parse_tokens(tokens_iter))
        elif token == ')':
            return result
        else:
            if token.startswith("'") and token.endswith("'"):
                token = token[1:-1]  # Remove enclosing quotes
            result.append(token)
    return result

def s_expr_to_dict(item):
    """Converts a standard S-expression item list into a dictionary."""
    if not isinstance(item, list):
        return item
    if not item:
        return None
    
    key = item[0]
    remaining = item[1:]
    
    if not remaining:
        return {key: None}
    
    if len(remaining) == 1 and not isinstance(remaining[0], list):
        return {key: remaining[0]}
    
    inner_dict = {}
    for sub_item in remaining:
        if isinstance(sub_item, list):
            res = s_expr_to_dict(sub_item)
            if isinstance(res, dict):
                inner_dict.update(res)
        else:
            inner_dict['content'] = sub_item
            
    return {key: inner_dict}

def generate_final_dict(parsed_structure):
    """Flattens the root list structures and generates the complete map."""
    while len(parsed_structure) == 1 and isinstance(parsed_structure[0], list) and isinstance(parsed_structure[0][0], list):
        parsed_structure = parsed_structure[0]
        
    root_dict = {}
    for item in parsed_structure:
        res = s_expr_to_dict(item)
        if isinstance(res, dict):
            root_dict.update(res)
    return root_dict

# --- New Functions ---

def parse_file_to_dict(file_path):
    """Reads a file path, parses its S-expression layout, and outputs a dict."""
    f = open(file_path, 'r')
    file_content = f.read()
    f.close()
    
    # Wrap content in a single root element to parse multiple top-level blocks safely
    tokens = tokenize(file_content)
    nested_lists = parse_tokens(iter(tokens))
    return generate_final_dict(nested_lists)

def decode_frame_data(parsed_dict):
    """
    Extracts the zlib content from the dictionary,
    decodes it from Base64, and decompresses it via zlib.
    """
    try:
        # Navigate down into the frames data block
        data_block = parsed_dict['ika-sprite']['frames']['data']
        base64_str = data_block['content']
        print(base64_str[:20])
        # 1. Decode from base64 string to compressed bytes
        compressed_bytes = base64.b64decode(base64_str)
        
        # 2. Decompress the zlib byte payload [1]
        decompressed_bytes = zlib.decompress(compressed_bytes)
        
        return decompressed_bytes
    except KeyError:
        raise KeyError("Could not find ['frames']['data']['content'] in the dictionary structure.")
    except Exception, e:
        raise ValueError("Failed to decode or decompress frame data: " + str(e))

