import pygame, sys, os
from pygame.locals import *


# Load functions borrowed from http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    # Scale the image for super cool retro feel
    width = image.get_width()
    height = image.get_height()
    image = pygame.transform.scale(image, (4*width, 4*height))
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound
