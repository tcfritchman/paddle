##### PADDLE #####
# game.py
# Thomas Fritchman

import pygame, sys, os, math, random
from constants import *
from utils import *
from pygame.locals import *
import levels

def main():
    # Initialize the screen
    print "Initializing..."
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Paddle")
    pygame.font.init()
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    menu(screen)
    game(screen)

def menu(screen):
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((GREEN))

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    menu_font = pygame.font.Font(None, 32)

    # Create Main menu text surf
    main_menu_surf = pygame.Surface(screen.get_size())
    main_menu_surf.set_colorkey(BLACK)
    main_menu_text = ["[F1] Play Game", "[F2] How To Play", "[F3] Acknowledgements", "[q] Quit"]
    line_space = 0
    for text in main_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        main_menu_surf.blit(textsurf, (MENU_TEXT_LOCATION[X], MENU_TEXT_LOCATION[Y] + line_space))
        line_space += MENU_TEXT_SPACING

    # Create level menu text surf
    level_menu_surf = pygame.Surface(screen.get_size())
    level_menu_surf.set_colorkey(BLACK)
    level_menu_text = ["[F1] Level 1", "[F2] Level 2", "[F3] Level 3", "[F4] Level 4", "[ESC] Back"]
    line_space = 0
    for text in level_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        level_menu_surf.blit(textsurf, (MENU_TEXT_LOCATION[X], MENU_TEXT_LOCATION[Y] + line_space))
        line_space += MENU_TEXT_SPACING

    # Blit text to screen
    clock = pygame.time.Clock()
    menu = "main"

    while 1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == K_q:
                    pygame.font.quit()
                    pygame.quit()
                if event.key == K_ESCAPE:
                    menu = "main"
                if event.key == K_F1:
                    if menu == "main":
                        menu = "level"
                if event.key == K_F2:
                    if menu == "main":
                        menu = "howto"
                if event.key == K_F3:
                    if menu == "main":
                        menu = "ack"

        screen.blit(background, (0, 0))
        if menu == "main":
            screen.blit(main_menu_surf, (0,0))
        elif menu == "level":
            screen.blit(level_menu_surf, (0,0))

        pygame.display.flip()

def game(screen):
    global fire_time
    fire_time = 0

    global rotation
    rotation = 0.0

    global ball_count
    ball_count = 1
    
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

    testLevel = [[1,0,1,0,0,0,0,0,1,0,1,0,1,0,1]]
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,12,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,2,1,0,1,0,1,0])
    testLevel.append([1,0,20,0,0,0,1,0,1,2,1,0,1,0,1])
    testLevel.append([1,0,0,0,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,4,1,0,1])
    testLevel.append([1,14,0,0,0,0,1,1,2,1,0,1,4,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,10,0,1,1,0,1,2,1,0,1,0])
    testLevel.append([1,0,15,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,0,21,0,1,1,2,1,0,1,0,1,0])
    testLevel.append([1,0,21,0,0,0,1,0,1,0,1,0,1,0,1])
    testLevel.append([1,0,0,16,0,0,1,1,0,1,0,1,0,1,0])
    testLevel.append([1,0,0,0,0,0,1,0,1,0,1,0,1,0,1])

    testLevel = levels.L2

    # Create game objects
    clock = pygame.time.Clock()
    hud = HUD()
    paddle = Paddle()
    testball = Ball(BALL_INITIAL_POSITION, 0)
    spawner = Spawner(testLevel)

    # Sprite groups
    allsprites = pygame.sprite.Group((paddle, testball))
    balls = pygame.sprite.Group((testball))
    tiles = pygame.sprite.Group()
    ball_powerups = pygame.sprite.Group()
    fire_powerups = pygame.sprite.Group()

    draw_tiles(testLevel, tiles)
    allsprites.add(tiles)

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
                    pygame.font.quit()
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
                if event.key == K_1:
                    ball = spawner.spawn_ball()
                    if ball != None:
                        balls.add(ball)
                        allsprites.add(ball)
                if event.key == K_2:
                    bp = spawner.spawn_ball_powerup()
                    if bp != None:
                        ball_powerups.add(bp)
                        allsprites.add(bp)
                if event.key == K_3:
                    fp = spawner.spawn_fire_powerup()
                    if fp != None:
                        fire_powerups.add(fp)
                        allsprites.add(fp)
                if event.key == K_i:
                    print fire_time

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
        hud.update()

        # Handle Collisions
        foreground_collision(balls, allsprites)
        paddle_collision(paddle, balls, hud)
        tile_collision(tiles, balls, allsprites, hud)
        if ball_powerup_collision(ball_powerups, balls, allsprites):
            ball = spawner.spawn_ball()
            if ball != None:
                balls.add(ball)
                allsprites.add(ball)
        if fire_powerup_collision(fire_powerups, balls, allsprites):
            fire_time = FIRE_POWERUP_EFFECT_TIME

        # Spawn powerups at random intervals
        if random.randint(0, BALL_POWERUP_CHANCE) == 0:
            bp = spawner.spawn_ball_powerup()
            if bp != None:
                ball_powerups.add(bp)
                allsprites.add(bp)
        if random.randint(0, FIRE_POWERUP_CHANCE) == 0:
            fp = spawner.spawn_fire_powerup()
            if fp != None:
                fire_powerups.add(fp)
                allsprites.add(fp)
        
        # Update timers
        if fire_time > 0:
             fire_time -= 1

        screen.blit(background, (0, 0))
        #screen.blit(text, (10, 10))
        allsprites.draw(screen)
        screen.blit(foreground, (0, 0))
        screen.blit(hud.get_image(), HUD_LOCATION)
        pygame.display.flip()

        if len(balls.sprites()) < 1:
            print "GAME OVER"

def paddle_collision(paddle, balls, hud):
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
            hud.reset()

def tile_collision(tiles, balls, allsprites, hud):
    ballList = balls.sprites()
    tileList = tiles.sprites()

    for ball in ballList:
        for tile in tileList:
            if pygame.sprite.collide_rect(tile, ball):
                if fire_time <= 0:
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
                if tile.get_value() == 1:
                    hud.register()
                elif tile.get_value() == 2:
                    hud.register_x2()
                elif tile.get_value() == 4:
                    hud.register_x4()
                tiles.remove(tile)
                allsprites.remove(tile)

def ball_powerup_collision(ball_powerups, balls, allsprites):
    ballList = balls.sprites()
    bpList = ball_powerups.sprites()

    for ball in ballList:
        for bp in bpList: 
            # First check if powerup has timed out..
            if bp.get_time() <= 0:
                ball_powerups.remove(bp)
                allsprites.remove(bp)
                return False
            if pygame.sprite.collide_rect(bp, ball):
                # Kill powerup
                ball_powerups.remove(bp)
                allsprites.remove(bp)
                return True
    return False

def fire_powerup_collision(fire_powerups, balls, allsprites):
    ballList = balls.sprites()
    fpList = fire_powerups.sprites()

    for ball in ballList:
        for fp in fpList: 
            # First check if powerup has timed out..
            if fp.get_time() <= 0:
                fire_powerups.remove(fp)
                allsprites.remove(fp)
                return False
            if pygame.sprite.collide_rect(fp, ball):
                # Kill powerup
                fire_powerups.remove(fp)
                allsprites.remove(fp)
                return True
    return False
        
def foreground_collision(balls, allsprites):
    ballList = balls.sprites()
    for ball in ballList:
        pos = ball.get_position()
        if math.sqrt(pow(pos[X] - CENTER[X], 2) + pow(pos[Y] - CENTER[Y], 2)) > FOREGROUND_RADIUS:
            # WE're outside the boundary circle
            print "BYE!"
            balls.remove(ball)
            allsprites.remove(ball)

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
        if fire_time > 1:
            pygame.draw.circle(self.image, YELLOW, [BALL_RADIUS, BALL_RADIUS], BALL_RADIUS)
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
        if fire_time == FIRE_POWERUP_EFFECT_TIME-1:
            pygame.draw.circle(self.image, YELLOW, [BALL_RADIUS, BALL_RADIUS], BALL_RADIUS)
            print "ON"
        elif fire_time == 1:
            pygame.draw.circle(self.image, RED, [BALL_RADIUS, BALL_RADIUS], BALL_RADIUS)
            print "OFF"

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
    def __init__(self, loc, val):
        pygame.sprite.Sprite.__init__(self)
        self.value = val
        self.image = pygame.Surface([TILE_WIDTH, TILE_HEIGHT])
        if self.value == 1:
            self.image.fill(GREEN)
        elif self.value == 2:
            self.image.fill(BLUE)
        elif self.value == 4:
            self.image.fill(VIOLET)
        else:
            self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.pos = loc

    def update(self):
        self.rect.center = self.pos

    def get_center(self):
        return self.rect.center

    def get_value(self):
        return self.value

class Ball_Powerup(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILE_WIDTH, TILE_HEIGHT])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = loc
        self.time = BALL_POWERUP_TIME

    def update(self):
        self.rect.center = self.pos
        self.time -= 1

    def get_center(self):
        return self.rect.center

    def get_time(self):
        return self.time

class Fire_Powerup(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILE_WIDTH, TILE_HEIGHT])
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.pos = loc
        self.time = FIRE_POWERUP_TIME 

    def update(self):
        self.rect.center = self.pos
        self.time -= 1

    def get_center(self):
        return self.rect.center

    def get_time(self):
        return self.time

class Spawner:
    def __init__(self, level):
        self.level = level
        self.ball_spawns = self._get_ball_locations(self.level)
        self.ball_powerup_spawns, self.fire_powerup_spawns = self._get_powerup_locations(self.level)

    def _get_ball_locations(self, level):
        locs = []
        field_top_left = (CENTER[X] - ((TILE_WIDTH * FIELD_WIDTH) / 2), CENTER[Y] - ((TILE_HEIGHT * FIELD_HEIGHT) / 2))
        
        y = field_top_left[Y] 
        for row in level:
            x = field_top_left[X]
            for tile in row:
                if tile >= 10 and tile <= 17:
                    locs.append(((x,y),tile))
                x += TILE_WIDTH
            y += TILE_HEIGHT
        return locs

    def _get_powerup_locations(self, level):
        ball_locs = []
        fire_locs = []
        field_top_left = (CENTER[X] - ((TILE_WIDTH * FIELD_WIDTH) / 2), CENTER[Y] - ((TILE_HEIGHT * FIELD_HEIGHT) / 2))
        
        y = field_top_left[Y] 
        for row in level:
            x = field_top_left[X]
            for tile in row:
                if tile == 20:
                    ball_locs.append(((x,y),tile))
                elif tile == 21:
                    fire_locs.append(((x,y),tile))
                x += TILE_WIDTH
            y += TILE_HEIGHT
        return ball_locs, fire_locs

    def spawn_ball(self):
        if len(self.ball_spawns) < 1:
            return None
        ball_id = random.randint(0, len(self.ball_spawns) - 1)
        loc = self.ball_spawns[ball_id][0]
        direction = (self.ball_spawns[ball_id][1] - 10)  * (PI/4)
        return Ball(loc, direction)

    def spawn_ball_powerup(self):
        if len(self.ball_powerup_spawns) < 1:
            return None
        pu_id = random.randint(0, len(self.ball_powerup_spawns) - 1)
        loc = self.ball_powerup_spawns[pu_id][0]
        # Spawn ball powerup
        return Ball_Powerup(loc)
        
    def spawn_fire_powerup(self):
        if len(self.fire_powerup_spawns) < 1:
            return None
        pu_id = random.randint(0, len(self.fire_powerup_spawns) - 1)
        loc = self.fire_powerup_spawns[pu_id][0]
        # Spawn fire powerup
        return Fire_Powerup(loc)

class HUD(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([HUD_WIDTH, HUD_HEIGHT])
        self.image.fill(CYAN)
        self.image.set_colorkey(CYAN)
        self.rect = self.image.get_rect()

        self.scorefont = pygame.font.Font(None, 24)
        self.multfont = pygame.font.Font(None, 40)

        self.score = 0
        self.add = SCORE_BLOCK
        self.addadd = SCORE_BLOCK 
        self.multiplier = 1

    def update(self):
        self.image.fill(CYAN)
        scoresurf = self.scorefont.render("Score " + str(self.score), 0, ORANGE)
        if self.multiplier == 2:
            multsurf = self.multfont.render("X" + str(self.multiplier), 0, BLUE)
        elif self.multiplier == 4:
            multsurf = self.multfont.render("X" + str(self.multiplier), 0, VIOLET)
        elif self.multiplier > 4:
            multsurf = self.multfont.render("X" + str(self.multiplier), 0, RED)
        else:
            multsurf = self.multfont.render("X" + str(self.multiplier), 0, GREEN)

        self.image.blit(scoresurf, SCORE_TEXT_LOCATION)
        self.image.blit(multsurf, MULT_TEXT_LOCATION)
        image = self.image.convert_alpha()

    def reset(self):
        self.add = SCORE_BLOCK
        self.addadd = SCORE_BLOCK
        self.multiplier = 1

    def register(self):
        self.add += self.addadd
        self.score += self.add

    def register_x2(self):
        if self.multiplier < 4:
            self.multiplier = 2
        self.addadd = self.multiplier * SCORE_BLOCK
        self.register()

    def register_x4(self):
        self.multiplier = 4
        self.addadd = self.multiplier * SCORE_BLOCK
        self.register()

    def get_score(self):
        return self.score

    def get_multiplier(self):
        return self.multiplier

    def get_image(self):
        return self.image

########## HELPER FUNCTIONS ###########
def draw_tiles(level, tileGroup):
    field_top_left = (CENTER[X] - ((TILE_WIDTH * FIELD_WIDTH) / 2), CENTER[Y] - ((TILE_HEIGHT * FIELD_HEIGHT) / 2))
    
    y = field_top_left[Y] 
    for row in level:
        x = field_top_left[X]
        for tile in row:
            if tile > 0 and tile < 10:
                tileGroup.add(Tile((x,y), tile))
            x += TILE_WIDTH
        y += TILE_HEIGHT

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
