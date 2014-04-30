##### PADDLE #####
# game.py
# Thomas Fritchman

import pygame, sys, os, math, random, time
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

def game(screen, level):
    global fire_time
    fire_time = 0

    global rotation
    rotation = 0.0

    global ball_count
    ball_count = 1

    global invincible
    invincible = False

    if level == levels.L1:
        background, butt = load_image("l1_background.png", None)    
        song = load_sound("l1_music.ogg")
    elif level == levels.L2:
        background, butt = load_image("l2_background.png", None)    
        song = load_sound("l2_music.ogg")
    elif level == levels.L3:
        background, butt = load_image("l3_background.png", None)    
        song = load_sound("l3_music.ogg")
    elif level == levels.L4:
        background, butt = load_image("l4_background.png", None)    
        song = load_sound("l4_music.ogg")

    hi_score = get_hi_score(level)
    
    try:
        song.play(100)
    except:
        pass

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

    testLevel = level

    # Create game objects
    clock = pygame.time.Clock()
    hud = HUD(hi_score)
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
                if event.key == K_ESCAPE:
                    song.stop()
                    return False
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == K_q:
                    pygame.font.quit()
                    pygame.quit()
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
                if event.key == K_4:
                    fire_time = FIRE_POWERUP_EFFECT_TIME
                if event.key == K_5:
                    invincible = True
            elif event.type == KEYUP:
                pass
            elif event.type == MOUSEMOTION: 
                rotation += pygame.mouse.get_rel()[X] / MOUSE_SENSE
                if rotation >= TWOPI:
                    rotation -= TWOPI
                elif rotation < 0:
                    rotation += TWOPI
                paddle.set_angle(rotation)

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
        allsprites.draw(screen)
        screen.blit(foreground, (0, 0))
        screen.blit(hud.get_image(), HUD_LOCATION)
        pygame.display.flip()

        # Determine whether game should be ended
        if len(tiles.sprites()) < 1:
            win_screen, wsr = load_image("you_win.png", -1)
            screen.blit(win_screen, (0,0))
            pygame.display.flip()
            time.sleep(2)
            if hud.get_score() > hi_score:
                write_hi_score(level, hud.get_score())
                hi_score_font = pygame.font.Font(None, 100)
                hi_score_surf = hi_score_font.render("HI SCORE "+str(hud.get_score()), 0, RED)
                screen.blit(hi_score_surf, (50, 300))
                pygame.display.flip()
                time.sleep(2)
            song.stop()
            return True
        if len(balls.sprites()) < 1:
            if invincible:
                ball = spawner.spawn_ball()
                if ball != None:
                    balls.add(ball)
                    allsprites.add(ball)
            else:
                lose_screen, lsr = load_image("game_over.png", -1)
                screen.blit(lose_screen, (0,0))
                pygame.display.flip()
                time.sleep(2)
                song.stop()
                return False

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
                    # Get side of collision
                    ballpos = ball.get_position()
                    tilepos = tile.get_center()
                    dy = ballpos[Y] - tilepos[Y]
                    dx = ballpos[X] - tilepos[X]
                    theta = math.atan2(dy, dx)
                    if theta > -PI/4 and theta <= PI/4:
                        # Right
                        ball.set_position((ballpos[X] + TILE_BUMP_DIST, ballpos[Y]))
                        ball.set_direction(PI - ball.get_direction())
                    elif theta > PI/4 and theta <= 3*PI/4:
                        # Bottom
                        # Bump down
                        ball.set_position((ballpos[X], ballpos[Y] + TILE_BUMP_DIST))
                        ball.set_direction(TWOPI - ball.get_direction())
                    elif theta > -3*PI/4 and theta <= -PI/4:
                        # Top
                        ball.set_position((ballpos[X], ballpos[Y] - TILE_BUMP_DIST))
                        ball.set_direction(2*PI - ball.get_direction())
                    else:
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
        pygame.draw.polygon(self.image, WHITE, vertices)

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
        self.flame1, self.rect = load_image('flame.png', -1)
        self.flame2, self.rect = load_image('flame2.png', -1)

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
            self.image = self.flame1 
        elif fire_time < FIRE_POWERUP_EFFECT_TIME-1 and fire_time > 1:
            if fire_time % 10 == 0:
                self.image = self.flame2
            elif fire_time % 5 == 0:
                self.image = self.flame1
        elif fire_time == 1:
            self.image = pygame.Surface([BALL_WIDTH, BALL_HEIGHT])
            self.image.set_colorkey(BLACK)
            pygame.draw.circle(self.image, RED, [BALL_RADIUS, BALL_RADIUS], BALL_RADIUS)

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
        if self.value == 1:
            self.image, self.rect = load_image('green_tile.png', -1)
        elif self.value == 2:
            self.image, self.rect = load_image('blue_tile.png', -1)
        elif self.value == 4:
            self.image, self.rect = load_image('violet_tile.png', -1)
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
        self.image, self.rect = load_image('balls.png', -1)
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
        self.image, self.rect = load_image('flame.png', -1)
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
    def __init__(self, hi):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([HUD_WIDTH, HUD_HEIGHT])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.scorefont = pygame.font.Font(None, 24)
        self.hiscorefont = pygame.font.Font(None, 20)
        self.multfont = pygame.font.Font(None, 40)

        self.score = 0
        self.hi_score = hi
        self.add = SCORE_BLOCK
        self.addadd = SCORE_BLOCK 
        self.multiplier = 1

    def update(self):
        self.image.fill(WHITE)
        scoresurf = self.scorefont.render("Score " + str(self.score), 0, ORANGE)
        hiscoresurf = self.hiscorefont.render("Hi Score " + str(self.hi_score), 0, CYAN)
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
        self.image.blit(hiscoresurf, HISCORE_TEXT_LOCATION)
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

def menu(screen):
    # Load background image
    background, brt = load_image("nebula.png", None)

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    menu_font = pygame.font.Font(None, 32)

    # Create Main menu text surf
    main_menu_surf = pygame.Surface(screen.get_size())
    main_menu_surf.set_colorkey(BLACK)
    main_menu_text = ["[F1] Play Game", "[F2] How To Play", "[ESC] Quit"]
    line_space = 0
    for text in main_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        main_menu_surf.blit(textsurf, (MENU_TEXT_LOCATION[X]+180, MENU_TEXT_LOCATION[Y] + line_space))
        line_space += MENU_TEXT_SPACING

    # Create level menu text surf
    level_menu_surf = pygame.Surface(screen.get_size())
    level_menu_surf.set_colorkey(BLACK)
    level_menu_text = ["[F1] Level 1      HI: " + str(get_hi_score(levels.L1))]
    level_menu_text.append("[F2] Level 2      HI: " + str(get_hi_score(levels.L2)))
    level_menu_text.append("[F3] Level 3      HI: " + str(get_hi_score(levels.L3)))
    level_menu_text.append("[F4] Level 4      HI: " + str(get_hi_score(levels.L4)))
    level_menu_text.append("[ESC] Back")

    line_space = 0
    for text in level_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        level_menu_surf.blit(textsurf, (MENU_TEXT_LOCATION[X], MENU_TEXT_LOCATION[Y] + line_space))
        line_space += MENU_TEXT_SPACING

    # Create how to play menu text surf
    menu_font = pygame.font.Font(None, 24)
    howto_menu_surf = pygame.Surface(screen.get_size())
    howto_menu_surf.set_colorkey(BLACK)
    howto_menu_text = ["Controls:"]
    howto_menu_text.append("Mouse: Rotate paddle")
    howto_menu_text.append("ESC: Return to menu")
    howto_menu_text.append("Q: Quit game")
    howto_menu_text.append("F: Fullscreen")
    howto_menu_text.append("")
    howto_menu_text.append("Cheats:")
    howto_menu_text.append("1: Spawn ball")
    howto_menu_text.append("2: Spawn ball powerup")
    howto_menu_text.append("3: Spawn flame powerup")
    howto_menu_text.append("4: Turn balls into flames")
    howto_menu_text.append("5: Invincibility mode")
    howto_menu_text.append("")
    howto_menu_text.append("                                                                                   ESC: Back")

    line_space = 0
    for text in howto_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        howto_menu_surf.blit(textsurf, (50, 25 + line_space))
        line_space += MENU_TEXT_SPACING

    howto_menu_text = ["How to play:"]
    howto_menu_text.append("Use your paddle to keep")
    howto_menu_text.append("the ball within the circular")
    howto_menu_text.append("bounds. Powerups will aid you")
    howto_menu_text.append("in your quest to destroy all the")
    howto_menu_text.append("blocks on the screen and to get")
    howto_menu_text.append("the highest score! The more")
    howto_menu_text.append("blocks you hit before the ball")
    howto_menu_text.append("hits the paddle, the faster ")
    howto_menu_text.append("your score increases. Get blue")
    howto_menu_text.append("and purple blocks to get an even")
    howto_menu_text.append("higher combo multiplier. Don't")
    howto_menu_text.append("let the ball leave the playing")
    howto_menu_text.append("field or else game over!!")

    line_space = 0
    for text in howto_menu_text:
        textsurf = menu_font.render(text, 0, WHITE)
        howto_menu_surf.blit(textsurf, (300, 25 + line_space))
        line_space += 28

    # Blit text to screen
    screen.blit(background, (0, 0))
    screen.blit(main_menu_surf, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    menu = "main"

    song = load_sound("menu_music.ogg")
    song.play(100)

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
                    if menu == "main":
                        pygame.font.quit()
                        pygame.quit()
                    menu = "main"
                if event.key == K_F1:
                    if menu == "main":
                        menu = "level"
                    elif menu == "level":
                        song.stop()
                        play_level(screen, 1)
                if event.key == K_F2:
                    if menu == "main":
                        menu = "howto"
                    elif menu == "level":
                        song.stop()
                        play_level(screen, 2)
                if event.key == K_F3:
                    if menu == "level":
                        song.stop()
                        play_level(screen, 3)
                if event.key == K_F4:
                    if menu == "level":
                        song.stop()
                        play_level(screen, 4)

        screen.blit(background, (0, 0))
        if menu == "main":
            screen.blit(main_menu_surf, (0,0))
        elif menu == "level":
            screen.blit(level_menu_surf, (0,0))
        elif menu == "howto":
            screen.blit(howto_menu_surf, (0,0))

        pygame.display.flip()

def get_hi_score(level):
    if level == levels.L1:
        file_name = "scores/l1"
    elif level == levels.L2:
        file_name = "scores/l2"
    elif level == levels.L3:
        file_name = "scores/l3"
    elif level == levels.L4:
        file_name = "scores/l4"
    try:
        f = open(file_name, "r")
    except:
        return 0
    s = int(f.read()) 
    f.close()
    return s
    
def write_hi_score(level, score):
    if level == levels.L1:
        file_name = "scores/l1"
    elif level == levels.L2:
        file_name = "scores/l2"
    elif level == levels.L3:
        file_name = "scores/l3"
    elif level == levels.L4:
        file_name = "scores/l4"
    try:
        open(file_name, "w").close()
        f = open(file_name, "w")
        f.write(str(score))
        f.close()
    except:
        return

def play_level(screen, level):
    level_list = [levels.L1, levels.L2, levels.L3, levels.L4]

    i = 1
    for l in level_list:
        if i < level:
            i += 1
            continue
        else:
            if not game(screen, l):
                break

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
