import sys
import os
import re
import base64
import zlib
from PIL import Image
import math

def SaveAllSprites():    
    savesprites=[]    
    raw_names = os.listdir()
    
    for f in raw_names:
        if f.endswith('ika-sprite'):
            savesprites.append(f)  
    
    for s in savesprites:        
        Sprite2TSX('', s)

'''        
def Sprite2TSX(folder, sprite_filename):
    decompressor = zlib.decompressobj()
    parsed_data = parse_file_to_dict(folder + sprite_filename)
    tile_width = int(parsed_data['ika-sprite']['frames']['dimensions']['width'])
    tile_height = int(parsed_data['ika-sprite']['frames']['dimensions']['height'])
    sname = sprite_filename[:-11]
    # Calculate exactly how many bytes make up ONE frame
    # 16 * 16 * 4 (RGBA) = 1024 bytes per frame
    bytes_per_frame = tile_width * tile_height * 4 
    
    rawframes = decode_frame_data(decompressor, parsed_data, bytes_per_frame)
    
    mode = "RGBA" 
    for i in range(len(rawframes)):
        # Reconstruct the image from our sliced raw byte blocks
        image = Image.frombytes(mode, (tile_width, tile_height), rawframes[i])
        image.save("output_"+sname+str(i)+".png")
        print("Savd output_"+sname+str(i)+".png")
'''

def Sprite2TSX(folder, sprite_filename, columns=4):

    parsed_data = parse_file_to_dict(folder + sprite_filename)
    
    tile_width = int(parsed_data['ika-sprite']['frames']['dimensions']['width'])
    tile_height = int(parsed_data['ika-sprite']['frames']['dimensions']['height'])
    hotx = int(parsed_data['ika-sprite']['frames']['hotspot']['x'])
    hoty = int(parsed_data['ika-sprite']['frames']['hotspot']['y'])
    hotwidth = int(parsed_data['ika-sprite']['frames']['hotspot']['width'])
    hotheight = int(parsed_data['ika-sprite']['frames']['hotspot']['height'])
    count = int(parsed_data['ika-sprite']['frames']['count'])
    
    bytes_per_frame = tile_width * tile_height * 4 
    rawframes = decode_frame_data(parsed_data, bytes_per_frame)
    sname = sprite_filename.replace('.ika-sprite', '')
    output_name =  sname + "_sheet.png"
    
    rows=stitch_frames_to_spritesheet(rawframes, tile_width, tile_height, columns, output_name)    

    s='''<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="''' + sname + '''" tilewidth="''' + str(tile_width) +  '''" tileheight="''' + str(tile_height) +  '''" tilecount="''' + str(count) +  '''" columns="''' + str(columns) +  '''">
 <image source="''' + sname + '_sheet.png' + '''" width="''' + str(tile_width * columns) +  ''' " height="''' + str(tile_height * rows) +  ''' "/>
 <tile id="0">
  <objectgroup>'''
    
    for i in range(count):
     s+='''<object id="''' + str(i) + '''" name="Hitbox" x="''' + str(hotx) + '''" y="''' + str(hoty) + '''" width="''' + str(hotwidth) + '''" height="''' + str(hotheight) + '''"/>'''
    
    s+='''</objectgroup>
 </tile>
</tileset>'''
    output_name = sname + ".tsx"
    #file(folder + output_name, 'wt').write(s)  
    with open(folder + output_name, "w", encoding="utf-8") as file:
        file.write(s)
    print("Saved tileset to " + str(output_name))


    
    

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


def decode_frame_data(parsed_dict, bytes_per_frame):
    data_block = parsed_dict['ika-sprite']['frames']['data']
    count = int(parsed_dict['ika-sprite']['frames']['count'])       
    base64_str = data_block['content']    

    compressed_bytes = base64.b64decode(base64_str)    
    decompressor = zlib.decompressobj()
    all_decompressed_bytes = decompressor.decompress(compressed_bytes)
    
    framedata = []
    
    for i in range(count):
        print("Starting frame"+str(i))
        start_idx = i * bytes_per_frame
        end_idx = start_idx + bytes_per_frame            
        frame_chunk = all_decompressed_bytes[start_idx:end_idx]
        framedata.append(frame_chunk)

    return framedata
    
def stitch_frames_to_spritesheet(framedata, tile_width, tile_height, columns, output_path="spritesheet.png"):
    total_frames = len(framedata)
    if total_frames == 0:
        print("No frame data provided to stitch!")
        return

    # 1. Calculate grid dimensions
    # If columns is larger than our total frames, cap it at total_frames
    actual_columns = min(columns, total_frames)
    # Ceil division to figure out how many rows we need (e.g., 5 frames / 2 columns = 3 rows)
    rows = math.ceil(total_frames / actual_columns)
    
    # 2. Calculate the pixel dimensions of the final canvas
    sheet_width = actual_columns * tile_width
    sheet_height = rows * tile_height
    
    # 3. Create a blank transparent image canvas
    spritesheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
    
    # 4. Loop through and paste each frame into place
    for i, frame_bytes in enumerate(framedata):
        # Determine the grid position (e.g., frame 5 in a 4-column grid is row 1, col 1)
        col_index = i % actual_columns
        row_index = i // actual_columns
        
        # Convert the raw byte block into a temporary PIL image object
        frame_image = Image.frombytes("RGBA", (tile_width, tile_height), frame_bytes)
        
        # Calculate the exact pixel coordinates for the top-left corner
        pos_x = col_index * tile_width
        pos_y = row_index * tile_height
        
        # Paste the frame onto our main canvas
        # (We pass frame_image twice because the second argument acts as an alpha mask, 
        # ensuring transparency behaves correctly)
        spritesheet.paste(frame_image, (pos_x, pos_y), frame_image)
    
    # 5. Save the final sheet
    spritesheet.save(output_path)
    print(f"Successfully stitched {total_frames} frames into a {actual_columns}x{rows} grid: {output_path}")
    return rows


SaveAllSprites()