#!/usr/bin/env python

"""
This program will generate a binary STL file with
a variable number of facets.
"""

from cdedtools import demparser, demtiler
from stltools  import stlgenerator

import argparse

# Command Line Options
parser = argparse.ArgumentParser(description="Generate an STL from a DEM file.")
parser.add_argument("-q", "--quality", dest="quality", default=2, help="The resolution of the resulting BMP. 1 will match the source resolution.")
parser.add_argument("-t", "--tile", dest="tile", default="none", help="Method to tile the DEM. 'none' will not tile.  Currently only 'square' and 'none' are supported.")
parser.add_argument("-ta", "--tilesacross", dest="tilesacross", default=1, help="How many horizontal tiles to cut the dem into. 1 will not tile the DEM in this axis.")
parser.add_argument("-td", "--tilesdown", dest="tilesdown", default=1, help="How many vertical tiles to cut the dem into. 1 will not tile the DEM in this axis.")
parser.add_argument("sourcefile",  help="Read data from SOURCEFILE", metavar="SOURCEFILE")
parser.add_argument("destination", help="Save the resultion Bitmap file as DESTINATION", metavar="DESTINATION")
args = parser.parse_args()

filetype = args.sourcefile[-3:]

def stl_save(heightmap, resolution, destination, tilenumber=0):
    """
    Take a height map and save it as an stl after downsampling it by 
    resolution.  Appends tile number to the destination filename.
    """
    for y in range(len(heightmap)):
        heightmap[y] = heightmap[y][::resolution]
        heightmap[y] = heightmap[y][::-1]
        for x in range(len(heightmap[y])):
            heightmap[y][x] = heightmap[y][x] / 4 / float(resolution)
            if heightmap[y][x] < 1:
                heightmap[y][x] = 1
    suffixindex = -1 # in case there is no suffix
    suffixindex = destination.rindex(".") # use rindex inc ase there are other . in the filename
    destination = destination[0:suffixindex] + str(tilenumber) +".stl"
    stlgenerator.generate_from_heightmap_array(heightmap, destination)

# Open the file and process the data
with open(args.sourcefile, "r") as f:
    if filetype == 'asc':
        print 'asc filetype'
        heightmap  = demparser.read_data_asc(f)
    else:
        heightmap  = demparser.read_data(f)
    resolution = int(args.quality)**2
    heightmap  = heightmap[::resolution]
    tilelist = demtiler.tile(heightmap,args.tilesdown,args.tilesacross,tiletype = args.tile)
    for tilenum, tile in enumerate(tilelist):
        stl_save(tile,resolution,args.destination,tilenum)
