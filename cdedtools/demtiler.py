"""
demtiler.py
This module contains functions to split up a dem into tiles.
"""

def tile(heightmap,tilesdown,tilesacross,tiletype = "square",demx = 0,demy = 0):
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
    
    You can optionally crop the dem heightmap to a given size 
    from the upperleft corner with demx and demy.  demx and demy specify
    the size in elements to crop the heightmap to.
    """
    tilesdown = int(tilesdown)
    tilesacross = int(tilesacross)
    demx = int(demx)
    demy = int(demy)
    
    if tiletype == "none":
        tilelist=[heightmap]
        return tilelist
    elif tiletype == "square":
        #importing here removes numpy dependancy for the no tiling case
        import numpy as np
        
        heightarray=np.array(heightmap)
        # Crop the array if requested
        if demy>0 and demx>0: 
            heightarray = heightarray[0:demy,0:demx]
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
    
    
