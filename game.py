import pygame, sys, os, math
from constants import *
from utils import *
from pygame.locals import *

def main():
    # Initialize the screen
    print "Initializing..."
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Paddle")
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((150,200,255))

    # Foreground boundary
    foreground = pygame.Surface(screen.get_size())
    foreground = foreground.convert()
    foreground.set_colorkey(BLUE)
    pygame.draw.circle(foreground, BLUE, CENTER, FOREGROUND_RADIUS)
    foreground = foreground.convert_alpha()
    

    # Blit to screen
    screen.blit(background, (0, 0))
    background.blit(foreground, (0, 0))
    pygame.display.flip()

    # Create game objects
    clock = pygame.time.Clock()
    paddle = Paddle()
    testball = Ball(CENTER, 0)

    # Sprite groups
    allsprites = pygame.sprite.Group((paddle, testball))

    # Globals
    rotation = 0.0

    while 1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                # FOR TESTING
                if event.key == K_ESCAPE:
                    main()
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == K_q:
                    pygame.quit()
            elif event.type == KEYUP:
                pass
            elif event.type == MOUSEMOTION: 
                rotation += pygame.mouse.get_rel()[X] / MOUSE_SENSE
                paddle.set_angle(rotation)
                #ROTATION = ROTATION % 360
                print "Rotation" + str(rotation)

        allsprites.update()
        
        screen.blit(background, (0, 0))
        #screen.blit(text, (10, 10))
        allsprites.draw(screen)
        screen.blit(foreground, (0, 0))

        pygame.display.flip()

# Paddle
# Location on screen determined by it's 'angle' attribute. Angle
# cooresponds to the angle of a line drawn from the center of the screen
# to the center of the paddle circle.
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, BLUE, [PADDLE_RADIUS, PADDLE_RADIUS], PADDLE_RADIUS)
        image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0 # Angle where paddle is located
        self._set_position(self.angle)

    def update(self):
        self._set_position(self.angle)
        self._draw_self(self.angle)

    def _set_position(self, angle):
        self.rect.center = [(CENTER[X] + PADDLE_SWING_RADIUS * math.cos(angle)), (CENTER[Y] + PADDLE_SWING_RADIUS * math.sin(angle))]

    def _draw_self(self, angle):
        # Draw base circle
        pygame.draw.circle(self.image, BLUE, [PADDLE_RADIUS, PADDLE_RADIUS], PADDLE_RADIUS)
        # Calculate position of 'shadow' circle
        shadow_pos = [int(PADDLE_RADIUS - (PADDLE_SWING_RADIUS * math.cos(angle))), int(PADDLE_RADIUS - (PADDLE_SWING_RADIUS * math.sin(angle)))]
        # Draw shadow circle on top of base circle using alpha color
        pygame.draw.circle(self.image, BLACK, shadow_pos, PADDLE_INNER_RADIUS)

        
    def set_angle(self, angle):
        self.angle = angle

# Ball
# Updates own position based on it's own speed and direction attributes.
class Ball(pygame.sprite.Sprite):
    def __init__(self, start_loc, start_dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BALL_WIDTH, BALL_HEIGHT])
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, RED, [BALL_RADIUS, BALL_RADIUS], BALL_RADIUS)
        image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = start_loc
        self.speed = BALL_SPEED
        self.direction = start_dir
        self.set_position(self.pos)

    def update(self):
        newx = self.pos[X] + self.speed * math.cos(self.direction)
        newy = self.pos[Y] + self.speed * math.sin(self.direction)
        self.pos = [newx, newy]
        self.rect.center = self.pos

    def set_position(self, pos):
        self.pos = pos

    def get_position(self):
        return self.pos

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_rect(self):
        return self.rect


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
