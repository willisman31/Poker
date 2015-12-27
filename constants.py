import pygame, mygui

WIDTH = 640
HEIGHT = 480

CAPTION = "Poker"

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

BACK_SCREEN = 60, 60, 100
BACK_BUTTON= 192, 192, 192
TEXT_BUTTON= 0, 0, 0

INITMONEY = 1000

TABLESCALE = 2
PICSIZE = (100, 100)

BG0 = pygame.image.load("images/bg0.jpg")
BG0 = pygame.transform.scale(BG0, (WIDTH, HEIGHT))
BG1 = pygame.image.load("images/bg1.jpg")
BG1 = pygame.transform.scale(BG1, (WIDTH, HEIGHT))
PKT1 = pygame.image.load("images/pkt0.png")
PKT1 = pygame.transform.scale(PKT1, (int(TABLESCALE*HEIGHT/2), HEIGHT/2)) #480 * 240
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




PICSIZE = (int(HEIGHT/4.8), int(HEIGHT/4.8)) # 100 * 100
TBLTOPLEFT = (int(HEIGHT/6), int(HEIGHT/6)) # (80, 80)
TBLWIDTH = HEIGHT
TBLHEIGHT = HEIGHT/2

BOY0 = (70,30)
BOY1 = (170,0)
BOY2 = (270,0)
BOY3 = (370,0)
BOY4 = (470,30)
BOY5 = (510,140)
BOY6 = (470,250)
BOY7 = (370,280)
BOY8 = (270,280)
BOY9 = (170,280)
BOY10= (70,250)
BOY11= (30,140)

BOYS = (BOY0, BOY1, BOY2, BOY3, BOY4, BOY5, BOY6, BOY7, BOY8, BOY9, BOY10, BOY11 )

#Order in which players sit
#ORDER= (7, 2, 10, 11, 4, 5, 0, 9, 1, 8, 3, 6)
ORDER = (8, 2, 11, 5, 4, 10, 0, 6, 1, 7, 3, 9)
