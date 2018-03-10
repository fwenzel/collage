import os


# Size of every image tile.
TILE_SIZE = 160, 240
RESIZE = True  # Resize files that don't match the above?

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

# Helper to resolve a subdirectory
subdir = lambda *d: os.path.join(os.path.dirname(__file__), *d)

# Location of input files
INPUT_DIR = subdir('images')

# Output file settings
OUTPUT_FILE = subdir('output', 'collage.jpg')
OUTPUT_QUALITY=95

# Image text settings
WRITE = True
FONT_FILE = subdir('fonts', 'Happy_Monkey', 'HappyMonkey-Regular.ttf')
FONT_SIZE = 20
FONT_COLOR = '#fff'
FONT_PADDING = 10  # Padding from bottom right tile corner, in px.

# Resolve image text
write_text = lambda no: str(no + 1)  # Default: Enumerate images.

# Post-processing of image. Default: Do nothing.
post_process = lambda img: None
