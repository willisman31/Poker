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




BG0 = pygame.image.load("bg0.jpg")
BG0 = pygame.transform.scale(BG0, (WIDTH, HEIGHT))
