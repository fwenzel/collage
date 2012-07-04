#!/usr/bin/env python
"""Make a grid from a set of input images."""

import glob
import math
import os
import sys

from PIL import Image


# All images should be this size already.
TILE_SIZE = 160, 240
# Column width of image grid. Rows will be determined automatically.
COLS = 5
# Tile offset.
# 0 will start at the top right, 1 will leave one empty tile, etc.
TILE_OFFSET = 0
# Outside padding (in px)
PADDING = 5
# Gap size between images (in px)
GAP = 2
# Background color
BGCOLOR = '#fff'
# Output dir
subdir = lambda d: os.path.join(os.path.dirname(__file__), d)
INPUT_DIR = subdir('images')
OUTPUT_DIR = subdir('output')
OUTPUT_FILENAME = 'collage.jpg'


def debug(s):
    sys.stderr.write('%s\n' % s)


def main():
    # List of input files.
    infiles = glob.glob(os.path.join(INPUT_DIR, '*.jpg'))
    debug('Found %s input files.' % len(infiles))

    # Create canvas.
    tile_count = len(infiles) + TILE_OFFSET
    ROWS = tile_count // COLS + (1 if tile_count % COLS else 0)
    imgsize = (2 * PADDING + TILE_SIZE[0] * COLS + GAP * (COLS - 1),
               2 * PADDING + TILE_SIZE[1] * ROWS + GAP * (ROWS - 1))
    img = Image.new('RGB', imgsize, BGCOLOR)
    debug('Creating a grid with %s columns and %s rows.' % (COLS, ROWS))

    imgno = TILE_OFFSET
    for tile_file in infiles:
        debug('Processing %s...' % tile_file)

        # Tile position.
        x = imgno % COLS
        y = imgno // COLS
        # Offsets.
        xoff = PADDING + x * (TILE_SIZE[0] + GAP)
        yoff = PADDING + y * (TILE_SIZE[1] + GAP)

        tile = Image.open(tile_file)

        # Place tile on canvas.
        img.paste(tile, (xoff, yoff))

        imgno += 1

    # Save output file.
    debug('Writing output file: %s' % OUTPUT_FILENAME)
    img.save(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME), quality=95)


if __name__ == '__main__':
    main()