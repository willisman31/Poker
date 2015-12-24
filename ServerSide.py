import sys, pygame, mygui, serverThread
from pygame.locals import *
from constants import *

pygame.init()

class PokerServer:

    def __init__(self, screen):

        self.serObj = serverThread.ServerThread()
        serIP = self.serObj.get_ip()
        serPort = self.serObj.get_port()
        serClients = self.serObj.get_num_of_clients()

        screen.fill(BACK_SCREEN)
        textServer, textServerRect = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Server", WHITE, None, WIDTH/2, HEIGHT/10)
        screen.blit(textServer, textServerRect)

        textIp, textIpRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Host IP : "+serIP, WHITE, None, WIDTH/2, HEIGHT/4)
        screen.blit(textIp, textIpRect)

        textPort, textPortRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Port : " + str(serPort), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/10)
        screen.blit(textPort, textPortRect)

        Button1 = mygui.Button()
        Button1.create_button(screen, BACK_BUTTON, WIDTH/3, HEIGHT/3.55, WIDTH/3.2,    HEIGHT/6.85,    0,  "Start Game", TEXT_BUTTON)

        while 1 :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            serClients = self.serObj.get_num_of_clients()
            textClients, textClientsRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "# of Clients : "+ str(serClients), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/5)
            pygame.draw.rect(screen, BACK_SCREEN, textClientsRect)
            screen.blit(textClients, textClientsRect)

            pygame.display.update()
