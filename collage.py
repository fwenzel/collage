#!/usr/bin/env python
"""
Make a grid from a set of input images.

All settings (below) can be overwritten in local_config.py.
"""

import glob
import math
import os
import sys

from PIL import Image, ImageFont, ImageDraw


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
subdir = lambda *d: os.path.join(os.path.dirname(__file__), *d)
INPUT_DIR = subdir('images')
OUTPUT_DIR = subdir('output')
OUTPUT_FILENAME = 'collage.jpg'
# Writing
NUMBER_START = 4  # None for no writing.
FONT_FILE = subdir('fonts', 'Happy_Monkey', 'HappyMonkey-Regular.ttf')
FONT_SIZE = 20
FONT_COLOR = '#fff'
FONT_PADDING = 10  # Padding from bottom right tile corner, in px.

# Import local configs, if present.
try:
    from local_config import *
except ImportError:
    pass


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

    # Initialize number.
    write_no = NUMBER_START
    if write_no is not None:
        font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

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

        # Write a number on the image, if desired.
        if write_no is not None:
            draw = ImageDraw.Draw(img)
            txt = str(write_no)

            # Calculate offsets.
            txtsize = draw.textsize(txt, font=font)
            font_xoff = xoff + TILE_SIZE[0] - txtsize[0] - FONT_PADDING
            font_yoff = yoff + TILE_SIZE[1] - txtsize[1] - FONT_PADDING

            # Finally, draw the number.
            draw.text((font_xoff, font_yoff), txt, font=font,
                      fill=FONT_COLOR)
            del draw

            write_no += 1

        imgno += 1

    # Save output file.
    debug('Writing output file: %s' % OUTPUT_FILENAME)
    img.save(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME), quality=95)


if __name__ == '__main__':
    main()