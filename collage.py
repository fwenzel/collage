#!/usr/bin/env python
"""
Generate a sequence from a set of input images.

All settings can be overwritten in settings_local.py.
"""

import glob
import math
import os
import sys
from importlib import import_module
from optparse import OptionParser

from PIL import Image, ImageFont, ImageDraw

import settings


def parse_files(option, opt, value, parser):
    valid_images = []
    images = value.split(',')
    for image_path in images:
        if os.path.isfile(image_path):
            valid_images.append(image_path)
    setattr(parser.values, option.dest, None if len(valid_images) < 1 else valid_images)

# Command-line options
parser = OptionParser()
parser.add_option('-i', '--input', dest="INPUT_DIR", action='store',
                  default=settings.INPUT_DIR, help='Specify input directory')
parser.add_option('-o', '--output', dest='OUTPUT_FILE', action='store',
                  default=settings.OUTPUT_FILE, help='Specify output file')
parser.add_option('-q', '--quality', dest='OUTPUT_QUALITY', action='store',
                  default=settings.OUTPUT_QUALITY, help='Specify quality of output file', type='int')
parser.add_option('--settings', dest='settings_module', action='store',
                  default='settings_local', help='Specify settings module')
parser.add_option('-f', '--files',
                  type='string',
                  action='callback',
                  dest='files',
                  help='Specify comma separated list paths of ordered images to sequence',
                  callback=parse_files)
(options, args) = parser.parse_args()


def debug(s):
    sys.stderr.write('%s\n' % s)


try:
    settings = import_module(options.settings_module, '.')
except ImportError:
    if options.settings_module != 'settings_local':
        debug('Error importing settings module "%s"!' %
              options.settings_module)
        sys.exit(1)


def main():
    # List of input files.
    infiles = options.files if options.files is not None else glob.glob(os.path.join(options.INPUT_DIR, '*.jpg'))
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
        debug('Processing %s...' % tile_file)

        # Tile position.
        pos = imgno + settings.TILE_OFFSET
        x = pos % COLS
        y = pos // COLS
        # Offsets.
        xoff = settings.PADDING + x * (settings.TILE_SIZE[0] + settings.GAP)
        yoff = settings.PADDING + y * (settings.TILE_SIZE[1] + settings.GAP)

        tile = Image.open(tile_file)

        # Resize image if necessary!
        if settings.RESIZE and tile.size != settings.TILE_SIZE:
            w_from, h_from = tile.size
            if (w_from / float(h_from) >
                settings.TILE_SIZE[0] / float(settings.TILE_SIZE[1])):
                w_to = settings.TILE_SIZE[0]
                h_to = int(w_to / float(w_from) * h_from)
            else:
                h_to = settings.TILE_SIZE[1]
                w_to = int(h_to / float(h_from) * w_from)
            tile = tile.resize((w_to, h_to), Image.ANTIALIAS)

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
    debug('Writing output file: %s' % options.OUTPUT_FILE)
    img.save(options.OUTPUT_FILE, quality=options.OUTPUT_QUALITY)


if __name__ == '__main__':
    main()
