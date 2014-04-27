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
    testball = Ball((200, 500), 3*PI/2)

    testLevel = [[1,0,1,0,0,0,0,0,1,0,1,0,1,0,1]]
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])


    # Sprite groups
    allsprites = pygame.sprite.Group((paddle, testball))
    balls = pygame.sprite.Group((testball))
    tiles = pygame.sprite.Group()

    draw_tiles(testLevel, tiles)
    allsprites.add(tiles)

    global rotation
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

                # FOR TESTING
                if event.key == K_LEFT:
                    rotation += 0.5
                    if rotation >= TWOPI:
                        rotation -= TWOPI
                    elif rotation < 0:
                        rotation += TWOPI
                    paddle.set_angle(rotation)
                if event.key == K_RIGHT:
                    rotation -= 0.5
                    if rotation >= TWOPI:
                        rotation -= TWOPI
                    elif rotation < 0:
                        rotation += TWOPI
                    paddle.set_angle(rotation)
                if event.key == K_r:
                    testball.set_position(CENTER)
                if event.key == K_w:
                    testball.set_direction(3*PI/2)
                if event.key == K_a:
                    testball.set_direction(PI)
                if event.key == K_s:
                    testball.set_direction(PI/2)
                if event.key == K_d:
                    testball.set_direction(0)

            elif event.type == KEYUP:
                pass
            elif event.type == MOUSEMOTION: 
                rotation += pygame.mouse.get_rel()[X] / MOUSE_SENSE
                if rotation >= TWOPI:
                    rotation -= TWOPI
                elif rotation < 0:
                    rotation += TWOPI
                paddle.set_angle(rotation)
                #print "Rotation" + str(rotation)

        allsprites.update()

        paddle_collision(paddle, balls)
        tile_collision(tiles, balls, allsprites)
        
        screen.blit(background, (0, 0))
        #screen.blit(text, (10, 10))
        allsprites.draw(screen)
        screen.blit(foreground, (0, 0))

        pygame.display.flip()

def paddle_collision(paddle, balls):
    ballList = balls.sprites()

    for ball in ballList:
        # When paddle collision - update ball direction.
        if pygame.sprite.collide_mask(paddle, ball):
            pos = ball.get_position()
            # Move out of paddle
            new_pos_x = pos[X] - (math.cos(paddle.angle) * PADDLE_BUMP_DIST)
            new_pos_y = pos[Y] - (math.sin(paddle.angle) * PADDLE_BUMP_DIST)
            ball.set_position((new_pos_x, new_pos_y))
            # Calculate new dirrection
            ball.set_direction(paddle.angle + PI + (paddle.angle - ball.get_direction()))

def tile_collision(tiles, balls, allsprites):
    ballList = balls.sprites()
    tileList = tiles.sprites()

    for ball in ballList:
        for tile in tileList:
            while pygame.sprite.collide_rect(tile, ball):
                print "kajsdf"
                # Get side of collision
                ballpos = ball.get_position()
                tilepos = tile.get_center()
                dy = ballpos[Y] - tilepos[Y]
                dx = ballpos[X] - tilepos[X]
                theta = math.atan2(dy, dx)
                if theta > -PI/4 and theta <= PI/4:
                    print "RIGHT"
                    # Right
                    ball.set_position((ballpos[X] + TILE_BUMP_DIST, ballpos[Y]))
                    ball.set_direction(PI - ball.get_direction())
                elif theta > PI/4 and theta <= 3*PI/4:
                    # Bottom
                    # Bump down
                    print "BOT"
                    ball.set_position((ballpos[X], ballpos[Y] + TILE_BUMP_DIST))
                    ball.set_direction(TWOPI - ball.get_direction())
                elif theta > -3*PI/4 and theta <= -PI/4:
                    # Top
                    print "TOP"
                    ball.set_position((ballpos[X], ballpos[Y] - TILE_BUMP_DIST))
                    ball.set_direction(2*PI - ball.get_direction())
                else:
                    print "LEFT"
                    # Left
                    ball.set_position((ballpos[X] - TILE_BUMP_DIST, ballpos[Y]))
                    ball.set_direction(PI - ball.get_direction())
                # Kill block
                tiles.remove(tile)
                allsprites.remove(tile)
                break










############ GAME OBJECTS ###########

# Paddle
# Location on screen determined by it's 'angle' attribute. Angle
# cooresponds to the angle of a line drawn from the center of the screen
# to the center of the paddle.

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([PADDLE_SURF_SIZE, PADDLE_SURF_SIZE])
        self.image.set_colorkey(BLACK)
        image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.angle = 0 # Angle where paddle is located
        self._set_position(self.angle)

    def update(self):
        self._set_position(self.angle)
        self._draw_self(self.angle)

    def _draw_self(self, angle):
        self.image.fill(BLACK)
        
        Ax = PADDLE_SURF_CENTER + (math.cos(PADDLE_HYP_ANGLE - self.angle) * PADDLE_HYP)
        Ay = PADDLE_SURF_CENTER - (math.sin(PADDLE_HYP_ANGLE - self.angle) * PADDLE_HYP)
        Bx = Ax - (math.cos(self.angle) * PADDLE_HEIGHT)
        By = Ay - (math.sin(self.angle) * PADDLE_HEIGHT)
        Cx = Ax - (math.sin(self.angle) * PADDLE_WIDTH)
        Cy = Ay + (math.cos(self.angle) * PADDLE_WIDTH)
        Dx = Cx - (Ax - Bx)
        Dy = Cy - (Ay - By)
        A = (int(Ax), int(Ay))
        B = (int(Bx), int(By))
        C = (int(Cx), int(Cy))
        D = (int(Dx), int(Dy))
        vertices = [A,B,D,C]
        pygame.draw.polygon(self.image, BLUE, vertices)

    def _set_position(self, angle):
        self.rect.center = [(CENTER[X] + PADDLE_SWING_RADIUS * math.cos(angle)), (CENTER[Y] + PADDLE_SWING_RADIUS * math.sin(angle))]

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

# Tile
class Tile(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILE_WIDTH, TILE_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = loc

    def update(self):
        self.rect.center = self.pos

    def get_center(self):
        return self.rect.center




########## HELPER FUNCTIONS ###########
def draw_tiles(level, tileGroup):
    field_top_left = (CENTER[X] - ((TILE_WIDTH * FIELD_WIDTH) / 2), CENTER[Y] - ((TILE_HEIGHT * FIELD_HEIGHT) / 2))
    
    y = field_top_left[Y] 
    for row in level:
        x = field_top_left[X]
        for tile in row:
            if tile == 1:
                tileGroup.add(Tile((x,y)))
            x += TILE_WIDTH
        y += TILE_HEIGHT



if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
