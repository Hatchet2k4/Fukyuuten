// Helper function to find or dynamically load a tileset by name
function getFirstTileFromTileset(tilesetName, map) {
    if (!tilesetName || !map) return null;

    for (let i = 0; i < map.tilesets.length; ++i) {
        let ts = map.tilesets[i];
        if (ts.name === tilesetName) {
            if (ts.tiles && ts.tiles.length > 0) return ts.tiles[0]; // Get the exact first tile object
        }
    }

    let mapDir = FileInfo.path(map.fileName);
    let tilesetPath = mapDir + "/tilesets/" + tilesetName + ".tsx"; 

    try {
        let externalTileset = tiled.open(tilesetPath);
        if (externalTileset) {
            map.addTileset(externalTileset);
            tiled.log(`Successfully imported and attached "${tilesetName}" to the map.`);
            if (externalTileset.tiles && externalTileset.tiles.length > 0) {
                return externalTileset.tiles[0];
            }
        }
    } catch (error) {
        tiled.log(`Error: Failed to load external file: ${error}`);
    }
    return null;
}

function generateMapHitboxes(asset) {
    if (!asset || !asset.isTileMap) return;

    const map = asset;

    // Iterate through layers to process source objects
    for (let i = 0; i < map.layerCount; ++i) {
        let sourceLayer = map.layerAt(i);
        
        // Skip processing if it's an old generated layer from previous script iterations
        if (!sourceLayer.isObjectLayer || sourceLayer.name === "Generated Hitboxes") continue;

        for (const obj of sourceLayer.objects) {
            let hotx = obj.property("hotx");
            let hoty = obj.property("hoty");
            let hotwidth = obj.property("hotwidth");
            let hotheight = obj.property("hotheight");
            let spriteClassName = obj.className; 

            if (hotwidth !== undefined && hotheight !== undefined) {
                let matchedTile = getFirstTileFromTileset(spriteClassName, map);
                
                if (matchedTile) {
                    // --- PART A: CONVERT OBJECT TO SPRITE ---
                    if (!obj.tile) {
                        obj.tile = matchedTile;
                        // Pivot fix for Tiled's bottom-left texture placement
                        obj.y = Number(obj.y) + Number(obj.height);
                    }

                    // --- PART B: EMBED HITBOX INTO TILE (GODOT LINK) ---
                    // Create a vector shape inside the tile asset's internal collision data array
                    let hitShape = new MapObject(MapObject.Rectangle);
                    
                    // Positions here are relative to the TILE sprite's top-left (0,0) bounds
                    hitShape.x = Number(hotx || 0);
                    hitShape.y = Number(hoty || 0);
                    hitShape.width = Number(hotwidth);
                    hitShape.height = Number(hotheight);
                    
                    // Give it a name or a 'type' property that YATI recognizes
                    hitShape.name = "Hitbox"; 
                    
                    // Inject the shape straight into the tileset template memory
                    // This creates a native collision container that Godot reads directly
                    matchedTile.objectGroup = new ObjectGroup();
                    matchedTile.objectGroup.addObject(hitShape);
                }
            }
        }
    }
    tiled.log(`Successfully embedded hitboxes natively into Godot-compatible tile data.`);
}

// 1. REGISTER MENU ACTION
let action = tiled.registerAction("DrawRectangles", function() {
    generateMapHitboxes(tiled.activeAsset);
});
action.text = "Process Custom Properties";
tiled.extendMenu("Edit", [{ action: "DrawRectangles" }]);

// 2. CONNECT TO MAP LOAD SIGNAL
//tiled.assetOpened.connect(function(asset) {
//    generateMapHitboxes(asset);
//});