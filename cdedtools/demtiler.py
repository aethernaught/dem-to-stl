"""
demtiler.py
This module contains functions to split up a dem into tiles.
"""

def tile(heightmap,tilesdown,tilesacross,tiletype = "square"):
    """
    Tile the preparsed heighmap. Returns an tilesdown by tilesacross list of tiles.
    tile(heightmap, tilesdown=2,tilesacross=3) returns
    [
    [ tile1, tile2, tile3],
    [ tile4, tile5, tile6]
    ]
    
    Note that if the heightmap doesn't divide into the tile size evenly,
    rows and columns of the heightmap will be ommited from the final 
    output to make the tiling fit.
    """
    tilesdown = int(tilesdown)
    tilesacross = int(tilesacross)
    
    if tiletype == "none":
        tilelist=[heightmap]
        return tilelist
    elif tiletype == "square":
        #importing here removes numpy dependancy for the no tiling case
        import numpy as np
        
        heightarray=np.array(heightmap)
        tilerows = heightarray.shape[0]/tilesdown
        tilecolumns = heightarray.shape[1]/tilesacross 
        tilelist=[]
        for row in range(tilesdown):
            for col in range(tilesacross):
                row0 = row * tilerows
                rowend = (row+1) * tilerows
                
                col0 = col * tilecolumns
                colend = (col+1) * tilecolumns
                
                tile = heightarray[row0:rowend,col0:colend]
                tile=tile.tolist()
                tilelist.append(tile)
        return tilelist
    else:
        raise Exception("Non square tiles currently unsupported")
    
    
