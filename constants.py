# constants.py - all game constants
# Thomas Fritchman
import pygame, math
from pygame.locals import *

# Screen
FPS = 60
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
CENTER = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
FOREGROUND_RADIUS = WINDOWWIDTH/2 - WINDOWWIDTH/50
BOUNDARY_RADIUS = WINDOWWIDTH/2

# Control
MOUSE_SENSE = 300.0

# Paddle
PADDLE_RADIUS = 160
PADDLE_INNER_RADIUS = 250
PADDLE_SWING_RADIUS = 250
PADDLE_SURF_SIZE = 320
PADDLE_SURF_CENTER = 160
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_HYP = math.sqrt(((PADDLE_WIDTH/2)*(PADDLE_WIDTH/2))+((PADDLE_HEIGHT/2)*(PADDLE_HEIGHT/2)))
PADDLE_HYP_ANGLE = math.atan2((PADDLE_WIDTH/2), (PADDLE_HEIGHT/2))
PADDLE_EDGE_ANGLE = math.atan2((PADDLE_WIDTH/2), PADDLE_SWING_RADIUS-(PADDLE_HEIGHT/2))
PADDLE_BUMP_DIST = 10

# Ball
BALL_INITIAL_POSITION = (450, 300)
BALL_RADIUS = 6
BALL_WIDTH = 2*BALL_RADIUS
BALL_HEIGHT = 2*BALL_RADIUS
BALL_SPEED = 2.4

# Tile
TILE_WIDTH = 20
TILE_HEIGHT = 20
TILE_BUMP_DIST = 5

# Field
FIELD_WIDTH = 15
FIELD_HEIGHT = 15

# Ball Powerup
BALL_POWERUP_TIME = 500
BALL_POWERUP_CHANCE = 2000

# Fire Powerup
FIRE_POWERUP_TIME = 500
FIRE_POWERUP_EFFECT_TIME = 300
FIRE_POWERUP_CHANCE = 3000

# HUD
HUD_LOCATION = (0, 0)
HUD_WIDTH = 150
HUD_HEIGHT = 100
SCORE_BLOCK = 10
SCORE_TEXT_LOCATION = (10, 50)
MULT_TEXT_LOCATION = (80, 10)



# Color constants
BLACK = Color(0, 0, 0)
GREY = Color(128, 128, 128)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
CYAN = Color(0, 255, 255)
YELLOW = Color(255, 255, 0)
VIOLET = Color(192, 0, 255)
ORANGE = Color(255, 128, 0)

# Misc.
X = 0
Y = 1
TWOPI = math.pi * 2
PI = math.pi
