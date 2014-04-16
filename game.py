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

    # Blit to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Create game objects
    clock = pygame.time.Clock()

    # Globals
    ROTATION = 0.0

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
                ROTATION += pygame.mouse.get_rel()[0] / 2000.0
                #ROTATION = ROTATION % 360
                print "Rotation" + str(ROTATION)

                
        
        #allsprites.update()
        
        screen.blit(background, (0, 0))
        #screen.blit(text, (10, 10))
        #allsprites.draw(screen)
        pygame.display.flip()



if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
