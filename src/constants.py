# Game title and description
GAME_TITLE = "Apprentice Log: Workshop Restoration"
GAME_DESCRIPTION = ""

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Grid dimensions (characters on screen)
GRID_WIDTH, GRID_HEIGHT = 60, 23

# UI panel & Map dimensions
HEADER_WIDTH, HEADER_HEIGHT = GRID_WIDTH, 1
MSG_WIDTH, MSG_HEIGHT = GRID_WIDTH, 5
MENU_WIDTH, MENU_HEIGHT = GRID_WIDTH, 1
UI_WIDTH = 26
MAP_WIDTH, MAP_HEIGHT = (
    GRID_WIDTH - UI_WIDTH,
    GRID_HEIGHT - HEADER_HEIGHT - MSG_HEIGHT - MENU_HEIGHT,
)
UI_HEIGHT = MAP_HEIGHT

# Padding in px
INNER_PADDING = 6
OUTER_PADDING = 6

# Font settings
FONT_SIZE = 30

# Symbols
WALL = "#"
FLOOR = "."
PLAYER = "@"
PLAYER_NAME = "Lina"

# Special Keywords with Colors
COLORED_WORDS = {}
