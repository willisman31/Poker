import sys, pygame, mygui, serverThread, serverGame, time
from pygame.locals import *
from constants import *

def main (screen, clientSocket):
    print "Inside clientGame file : Method main()"
    #screen.fill(BACK_SCREEN)


    #pygame.quit()
    #sys.exit()

    bg1 = pygame.image.load("bg1.jpg")
    bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
    screen.blit(bg1, (0,0))
    pygame.display.update()
    time.sleep(5)

    # init_recv()
    # update_game()
    #
    # while 1:
    #     if turn == myturn:
    #         do_some()
    #         send_server()
    #     else:
    #         recv_broadcast()
    #         update_game()
