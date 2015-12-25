import sys, pygame, mygui, serverThread, serverGame, time
from pygame.locals import *
from constants import *

def main (screen, clientSocket):
    print "Inside clientGame file : Method main()"
    screen.fill(BACK_SCREEN)
    pygame.display.update()
    time.sleep(5)
    pygame.quit()
    sys.exit()

    init_recv()
    update_game()

    while 1:
        if turn == myturn:
            do_some()
            send_server()
        else:
            recv_broadcast()
            update_game()
