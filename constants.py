import pygame, mygui

WIDTH = 640
HEIGHT = 480

CAPTION = "Poker"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

BACK_SCREEN = 60, 60, 100
BACK_BUTTON= 192, 192, 192
TEXT_BUTTON= 0, 0, 0

INITMONEY = 1000

TABLESCALE = 2
PICSIZE = (100, 100)

CARDLENIMG = 43
CARDWIDIMG = 62
CARDLEN = 36
CARDWID = 49
CARDS= pygame.image.load("images/card_spritesheet.png")


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
but2 = pygame.image.load("images/but0.png")
but2 = pygame.transform.scale(but2, (120,30))
but3 = pygame.image.load("images/but4.png")
but3 = pygame.transform.scale(but3, (200,50))

alpha = 180
but4 = pygame.image.load("images/but6.png")
but4 = pygame.transform.scale(but4, (120,30))
but4.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

but5 = pygame.image.load("images/but6.png")
but5 = pygame.transform.scale(but5, (120,30))

but6 = pygame.image.load("images/but7.png")
but6 = pygame.transform.scale(but6, (120,30))
but7 = pygame.image.load("images/but3.png")
but7 = pygame.transform.scale(but7, (90,30))
but8 = pygame.image.load("images/but8.png")
but8 = pygame.transform.scale(but8, (90,30))

but9 = pygame.image.load("images/but7.png")
but9 = pygame.transform.scale(but9, (120,30))
but9.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)

sl1 = pygame.image.load("images/slider0.png")
sl1 = pygame.transform.scale(sl1, (200,4))
sl2 = pygame.image.load("images/slider1.png")
sl2 = pygame.transform.scale(sl2, (39,20))




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
ORDER = (8, 2, 11, 5, 4, 10, 0, 6, 1, 7, 3, 9)
