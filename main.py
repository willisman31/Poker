import sys, pygame, mygui, ServerSide, ClientSide
from pygame.locals import *
from constants import *

pygame.init()

pygame.display.set_caption("Poker")
width, height = size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

screen.fill(BACK_SCREEN)

textSurfaceObj, textRectObj = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Welcome", WHITE, None, WIDTH/2, HEIGHT/10)
screen.blit(textSurfaceObj, textRectObj)

Button1 = mygui.Button()
Button2 = mygui.Button()
#Parameters:      surface,      color,       x,   y,   length, height, width,    text,      text_color
Button1.create_button(screen, BACK_BUTTON, WIDTH/3, HEIGHT/3.55, WIDTH/3.2,    HEIGHT/6.85,    0,        "Server", TEXT_BUTTON)
Button2.create_button(screen, BACK_BUTTON, WIDTH/3, HEIGHT/1.88, WIDTH/3.2,    HEIGHT/6.85,    0,        "Client", TEXT_BUTTON)

quit = False
while not quit :
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if Button1.pressed(pygame.mouse.get_pos()):
                state = 1
                quit = True
                break

            if Button2.pressed(pygame.mouse.get_pos()):
                state = 2
                quit = True
                break

    pygame.display.update()

if state == 1:
    ServerSide.PokerServer(screen)
elif state == 2:
    ClientSide.PokerClient(screen)
