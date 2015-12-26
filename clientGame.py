import sys, pygame, mygui, serverThread, serverGame, time
from pygame.locals import *
from constants import *

def main (screen, clientSocket):
    print "Inside clientGame file : Method main()"

    bg1 = pygame.image.load("images/bg1.jpg")
    bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
    screen.blit(bg1, (0,0))
    pygame.display.update()
    #time.sleep(5)

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

def test(screen):

    PICSIZE = (int(HEIGHT/4.8), int(HEIGHT/4.8)) # 100 * 100
    TBLTOPLEFT = (int(HEIGHT/6), int(HEIGHT/6)) # (80, 80)
    TBLWIDTH = HEIGHT
    TBLHEIGHT = HEIGHT/2
    BOY0 = (70,30)
    BOY1 = (170,0)
    BOY2 = (270,0)
    BOY3 = (370,0)
    BOY4 = (470,30)
    BOY5 = (70,250)
    BOY6 = (170,280)
    BOY7 = (270,280)
    BOY8 = (370,280)
    BOY9 = (470,250)
    BOY10= (30,140)
    BOY11= (510,140)


    bg1 = pygame.image.load("images/bg1.jpg")
    bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))

    tableScale = 2
    pkt1 = pygame.image.load("images/pkt0.png")
    pkt1 = pygame.transform.scale(pkt1, (int(tableScale*HEIGHT/2), HEIGHT/2)) #480 * 240

    boy0 = pygame.image.load("images/boy1.png")
    boy0 = pygame.transform.scale(boy0, PICSIZE)

    boy1 = pygame.image.load("images/boy2.png")
    boy1 = pygame.transform.scale(boy1, PICSIZE)

    boy2 = pygame.image.load("images/boy3.png")
    boy2 = pygame.transform.scale(boy2, PICSIZE)

    boy3 = pygame.image.load("images/boy4.png")
    boy3 = pygame.transform.scale(boy3, PICSIZE)


    but1 = pygame.image.load("images/but1.png")
    but1 = pygame.transform.scale(but1, (90,30))


    screen.blit(bg1, (0,0))
    screen.blit(pkt1, TBLTOPLEFT)

    screen.blit(boy0, BOY0)
    screen.blit(boy1, BOY1)
    screen.blit(boy2, BOY2)
    screen.blit(boy2, BOY3)
    screen.blit(boy1, BOY4)

    screen.blit(boy1, BOY5)
    screen.blit(boy3, BOY6)
    screen.blit(boy3, BOY7)
    screen.blit(boy1, BOY8)
    screen.blit(boy1, BOY9)

    screen.blit(boy1, BOY10)
    screen.blit(boy1, BOY11)

    screen.blit(but1, (35,226))
    screen.blit(but1, (75,336))
    screen.blit(but1, (75,116))
    screen.blit(but1, (175,86))
    screen.blit(but1, (275,86))
    screen.blit(but1, (375,86))

    textPort, textPortRect = mygui.print_text('freesansbold.ttf', 13, "$100,234", WHITE, None,80,248 )
    textPort2, textPortRect2 = mygui.print_text('freesansbold.ttf', 13, "Kariryaa", WHITE, None,80,234 )
    screen.blit(textPort, textPortRect)
    screen.blit(textPort2, textPortRect2)


    pygame.display.update()
    time.sleep(5)


    #
    # screen.blit(bg1, BOY0, BOY0+PICSIZE)
    # screen.blit(pkt1, TBLTOPLEFT, (0,0,PICSIZE[0]-TBLTOPLEFT[0]+BOY0[0],PICSIZE[1]-TBLTOPLEFT[1]+BOY0[1]))

    # screen.blit(bg1, BOY1, BOY1+PICSIZE)
    # screen.blit(pkt1, (BOY1[0],TBLTOPLEFT[1]), (BOY1[0]-TBLTOPLEFT[0],0,PICSIZE[0],BOY1[1]+PICSIZE[1]-TBLTOPLEFT[1]))

    # screen.blit(bg1, BOY2, BOY2+PICSIZE)
    # screen.blit(pkt1, (BOY2[0],TBLTOPLEFT[1]), (BOY2[0]-TBLTOPLEFT[0],0,PICSIZE[0],BOY2[1]+PICSIZE[1]-TBLTOPLEFT[1]))

    # screen.blit(bg1, BOY3, BOY3+PICSIZE)
    # screen.blit(pkt1, (BOY3[0],TBLTOPLEFT[1]), (BOY3[0]-TBLTOPLEFT[0],0,PICSIZE[0],BOY3[1]+PICSIZE[1]-TBLTOPLEFT[1]))

    # screen.blit(bg1, BOY4, BOY4+PICSIZE)
    # screen.blit(pkt1, (BOY4[0],TBLTOPLEFT[1]), (BOY4[0]-TBLTOPLEFT[0],0,PICSIZE[0]-TBLWIDTH+BOY4[0],PICSIZE[1]-TBLTOPLEFT[1]+BOY4[1]))

    # screen.blit(bg1, BOY10, BOY10+PICSIZE)
    # screen.blit(pkt1, (TBLTOPLEFT[0],BOY10[1]), (0,BOY10[1]-TBLTOPLEFT[1],PICSIZE[0]-TBLTOPLEFT[0]+BOY10[0],PICSIZE[1]))

    # screen.blit(bg1, BOY11, BOY11+PICSIZE)
    # screen.blit(pkt1, (BOY11[0],BOY11[1]), (BOY11[0]-TBLTOPLEFT[0],BOY11[1]-TBLTOPLEFT[1],TBLWIDTH+TBLTOPLEFT[0]-BOY11[0],PICSIZE[1]))




    # screen.blit(bg1, BOY5, BOY5+PICSIZE)
    # screen.blit(pkt1, (TBLTOPLEFT[0],BOY5[1]), (0,BOY5[1]-TBLTOPLEFT[1],PICSIZE[0]-TBLTOPLEFT[0]+BOY5[0],TBLTOPLEFT[1]+PICSIZE[1]-BOY5[1]))

    # screen.blit(bg1, BOY6, BOY6+PICSIZE)
    # screen.blit(pkt1, (BOY6[0],BOY6[1]), (BOY6[0]-TBLTOPLEFT[0],BOY6[1]-TBLTOPLEFT[1],PICSIZE[0],TBLTOPLEFT[1]+PICSIZE[1]-BOY6[1]))
    #
    # screen.blit(bg1, BOY7, BOY7+PICSIZE)
    # screen.blit(pkt1, (BOY7[0],BOY7[1]), (BOY7[0]-TBLTOPLEFT[0],BOY7[1]-TBLTOPLEFT[1],PICSIZE[0],TBLTOPLEFT[1]+PICSIZE[1]-BOY7[1]))
    #
    # screen.blit(bg1, BOY8, BOY8+PICSIZE)
    # screen.blit(pkt1, (BOY8[0],BOY8[1]), (BOY8[0]-TBLTOPLEFT[0],BOY8[1]-TBLTOPLEFT[1],PICSIZE[0],TBLTOPLEFT[1]+PICSIZE[1]-BOY8[1]))
    #
    # screen.blit(bg1, BOY9, BOY9+PICSIZE)
    # screen.blit(pkt1, (BOY9[0],BOY9[1]), (BOY9[0]-TBLTOPLEFT[0],BOY9[1]-TBLTOPLEFT[1],TBLWIDTH+TBLTOPLEFT[0]-BOY9[0],TBLTOPLEFT[1]+PICSIZE[1]-BOY9[1]))





    pygame.display.update()
    time.sleep(5)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    test(screen)
