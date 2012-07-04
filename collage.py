#!/usr/bin/env python
"""
Make a grid from a set of input images.

All settings can be overwritten in settings_local.py.
"""

import glob
import math
import os
import sys

from PIL import Image, ImageFont, ImageDraw

import settings


def debug(s):
    sys.stderr.write('%s\n' % s)


def main():
    # List of input files.
    infiles = glob.glob(os.path.join(settings.INPUT_DIR, '*.jpg'))
    debug('Found %s input files.' % len(infiles))

    # Create canvas.
    tile_count = len(infiles) + settings.TILE_OFFSET
    COLS = settings.COLS
    ROWS = tile_count // COLS + (1 if tile_count % COLS else 0)
    imgsize = (2 * settings.PADDING + settings.TILE_SIZE[0] * COLS +
               settings.GAP * (COLS - 1),
               2 * settings.PADDING + settings.TILE_SIZE[1] * ROWS +
               settings.GAP * (ROWS - 1))
    img = Image.new('RGB', imgsize, settings.BGCOLOR)
    debug('Creating a grid with %s columns and %s rows.' % (COLS, ROWS))

    # Initialize writing.
    if settings.WRITE:
        font = ImageFont.truetype(settings.FONT_FILE, settings.FONT_SIZE)

    imgno = 0
    for tile_file in infiles:
        pos = imgno + settings.TILE_OFFSET
        debug('Processing %s...' % tile_file)

        # Tile position.
        x = pos % COLS
        y = pos // COLS
        # Offsets.
        xoff = settings.PADDING + x * (settings.TILE_SIZE[0] + settings.GAP)
        yoff = settings.PADDING + y * (settings.TILE_SIZE[1] + settings.GAP)

        tile = Image.open(tile_file)

        # Place tile on canvas.
        img.paste(tile, (xoff, yoff))

        # Write a number on the image, if desired.
        if settings.WRITE:
            draw = ImageDraw.Draw(img)
            txt = settings.write_text(imgno)

            # Calculate offsets.
            txtsize = draw.textsize(txt, font=font)
            font_xoff = (xoff + settings.TILE_SIZE[0] - txtsize[0] -
                         settings.FONT_PADDING)
            font_yoff = (yoff + settings.TILE_SIZE[1] - txtsize[1] -
                         settings.FONT_PADDING)

            # Finally, draw the number.
            draw.text((font_xoff, font_yoff), txt, font=font,
                      fill=settings.FONT_COLOR)
            del draw

        imgno += 1

    # Post-process image.
    settings.post_process(img)

    # Save output file.
    debug('Writing output file: %s' % settings.OUTPUT_FILENAME)
    img.save(os.path.join(settings.OUTPUT_DIR, settings.OUTPUT_FILENAME),
             quality=95)


if __name__ == '__main__':
    main()
