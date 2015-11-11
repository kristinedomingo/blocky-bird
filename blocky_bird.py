import pygame, sys
import random
import math
import neural_network
from pygame.locals import *

pygame.init()

# -----------------
# Window Attributes
# -----------------

FPS = 30
WINDOWWIDTH = 400
WINDOWHEIGHT = 600

global FPSCLOCK, DISPLAYSURF
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Blocky Bird!")

# --------------
# Color Settings
# --------------

#            R    G    B
WHITE    = (255, 255, 255)
GREEN    = (0,   255,   0)
YELLOW   = (255, 255,   0)
DARKBLUE = (0,   0,   150)

BGCOLOR = DARKBLUE
BIRDCOLOR = YELLOW
PIPECOLOR = GREEN
TEXTCOLOR = WHITE
PIPEHOLECOLOR = DARKBLUE

BIRDSIZE = 40

# -------------
# Game Function
# -------------
def game_function(ann, display):   

    # The seed MUST be the same for all generations, because the AI is learning
    # this SPECIFIC Blocky Bird setup
    random.seed(0)

    # ----------
    # Game State
    # ----------

    # start bird position
    bird_x = 100
    bird_y = WINDOWHEIGHT / 2

    # start bird velocity
    bird_vx = 0
    bird_vy = 9

    # start bird acceleration
    bird_ax = 0
    bird_ay = 2.5

    # start score
    score = 0

    # start pipe solid position, top right corner
    pipe_solid_x = 700
    pipe_solid_y = 0

    # pipe hole height
    pipe_hole_height = 190

    # pipe hole position, top right corner
    pipe_hole_x = pipe_solid_x
    pipe_hole_y = random.randint(50, (WINDOWHEIGHT - pipe_hole_height - 50))

    # pipe velocity
    pipe_vx = -16
    pipe_vy = 0

    # pipe width and height
    pipe_width = 60
    pipe_height = WINDOWHEIGHT

    # margin between pipes
    pipe_margin = pipe_width * 4

    # text 
    fontObj = pygame.font.SysFont('courbd.ttf', 32)
    textScore = str(score)
    label = fontObj.render(textScore, 1, WHITE)

    playing = True

    # main game loop
    while playing == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == KEYDOWN and event.key == K_SPACE:
                bird_vy = -20

        # distance from top of bird to top of pipe hole
        y_distance_top = pipe_hole_y - bird_y

        # distance from bottom of bird to bottom of pipe hole
        y_distance_bottom = (bird_y + BIRDSIZE) - (pipe_hole_y + pipe_hole_height)

        # feed sensors to the ANN
        sensors = [y_distance_top, y_distance_bottom, 1.0]
        output = ann.run(sensors)

        # handle output
        # if(output < 0):
        #     bird_vy = -20

        # bird movement
        bird_x += bird_vx
        bird_y += bird_vy
        
        bird_vx += bird_ax
        bird_vy += bird_ay
        
        # pipe movement
        pipe_solid_x += pipe_vx
        pipe_solid_y += pipe_vy
        pipe_hole_x += pipe_vx
        pipe_hole_y += pipe_vy
        
        # ---------
        # collision
        # ---------

        # if right/top side of bird hits a pipe
        if((bird_x + BIRDSIZE > pipe_solid_x) and 
           (bird_y < pipe_hole_y)             and
           (bird_x < pipe_solid_x + pipe_width)):
            playing = False

        # if the bottom side of the bird hits a pipe
        if((bird_x + BIRDSIZE > pipe_solid_x)                   and
           (bird_y + BIRDSIZE > pipe_hole_y + pipe_hole_height) and
           (bird_x < pipe_solid_x + pipe_width)):
            playing = False
        
        # new pipe
        if(pipe_solid_x < -(pipe_width)):
            pipe_solid_x = WINDOWWIDTH
            pipe_hole_x = pipe_solid_x
            pipe_hole_y = random.randint(20, WINDOWHEIGHT - pipe_hole_height - 20)
            score += 1
        
        # ------------
        # draw objects
        # ------------

        if(display):
            # background color
            DISPLAYSURF.fill(BGCOLOR)
            # pipe solid
            pygame.draw.rect(DISPLAYSURF, GREEN, (pipe_solid_x, pipe_solid_y, pipe_width, pipe_height))

            # pipe hole
            pygame.draw.rect(DISPLAYSURF, PIPEHOLECOLOR, ((pipe_hole_x, pipe_hole_y, pipe_width, pipe_hole_height)))

            # bird
            pygame.draw.rect(DISPLAYSURF, YELLOW, (bird_x, bird_y, BIRDSIZE, BIRDSIZE))

            # text (score)
            textScore = str(score)
            label = fontObj.render(textScore, 1, WHITE)

            # update display
            DISPLAYSURF.blit(label, (50, 50))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    return score
    
if (__name__=='__main__'):
    from neural_network import neuron
    ann = neuron()
    print game_function(ann, True)
    pygame.quit()
    sys.exit()
#game_function()