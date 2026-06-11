
import sys
import os
import re
import base64
import zlib
from PIL import Image


def SaveAllSprites():    
    savesprites=[]    
    raw_names = os.listdir('sprites')
    
    for f in raw_names:
        if f.endswith('ika-sprite'):
            savesprites.append(f)  
    
    savesprites=["arrow.ika-sprite"]
    
    for s in savesprites:        
        Sprite2TSX('sprites/', s)
        
def Sprite2TSX(folder, sprite):
   
    s=''
    sname = sprite[:-11]
    parsed_data = parse_file_to_dict(folder+sprite)
    
    tile_width = int(parsed_data['ika-sprite']['frames']['dimensions']['width'])
    tile_height = int(parsed_data['ika-sprite']['frames']['dimensions']['height'])
    hotx = int(parsed_data['ika-sprite']['frames']['hotspot']['x'])
    hoty = int(parsed_data['ika-sprite']['frames']['hotspot']['x'])
    hotwidth = int(parsed_data['ika-sprite']['frames']['hotspot']['width'])
    hotheight = int(parsed_data['ika-sprite']['frames']['hotspot']['height'])
    count = int(parsed_data['ika-sprite']['frames']['count'])
    
    
    #columns = (image.width - 1) // (tile_width + 1)
    #rows = (image.height - 1) // (tile_height + 1)
   
    
    #bigimage.Save(folder+sname+'_decompressed.png')
    mode = "RGBA" 
    rawframes = decode_frame_data(parsed_data)
    
    for i in range(len(rawframes)):
        # Reconstruct the image from raw bytes
        image = Image.frombytes(mode, (width, height), rawframes[i])
        
        image.save("output_frame"+str(i)+".png")
    

    
    

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

decompressor = zlib.decompressobj()

def decode_frame_data(parsed_dict):
    # Navigate down into the frames data block
    data_block = parsed_dict['ika-sprite']['frames']['data']
    count = int(parsed_dict['ika-sprite']['frames']['count'])       
    base64_str = data_block['content']    

    # 1. Decode from base64 string to compressed bytes
    compressed_bytes = base64.b64decode(base64_str)    
    framedata=[]
    for i in range(count):
        decompressed_frame = decompressor.decompress(compressed_bytes)                
        decompressed_frame += decompressor.flush()
        framedata.append(decompressed_frame)
        
    return framedata
    



SaveAllSprites()