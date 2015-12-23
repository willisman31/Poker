import sys, pygame, mygui
from pygame.locals import *
from constants import *

pygame.init()

class PokerServer:

    def __init__(self, screen):

        screen.fill(BACK_SCREEN)
        textSurfaceObj, textRectObj = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Server", WHITE, None, WIDTH/2, HEIGHT/10)
        screen.blit(textSurfaceObj, textRectObj)

        while 1 :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
