import os


# All images should be this size already.
TILE_SIZE = 160, 240
RESIZE = False  # Resize files that don't match the above?

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
OUTPUT_FILE = subdir('output', 'collage.jpg')

# Writing
WRITE = True
FONT_FILE = subdir('fonts', 'Happy_Monkey', 'HappyMonkey-Regular.ttf')
FONT_SIZE = 20
FONT_COLOR = '#fff'
FONT_PADDING = 10  # Padding from bottom right tile corner, in px.
write_text = lambda no: str(no + 1)  # Default: Enumerate images.

# Post-processing of image. Default: Do nothing.
post_process = lambda img: None
