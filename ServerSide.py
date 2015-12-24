import sys, pygame, mygui, serverThread, serverGame
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

        isButton = False

        quit = False
        while not quit :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if Button1.pressed(pygame.mouse.get_pos()):
                        quit = True
                        break

            serClients = self.serObj.get_num_of_clients()
            if serClients>0 :
                if not isButton:
                    isButton = True
                    Button1 = mygui.Button()
                    Button1.create_button(screen, BACK_BUTTON, WIDTH/3, 2*HEIGHT/3, WIDTH/3.2,    HEIGHT/6.85,    0,  "Start", TEXT_BUTTON)
            else:
                if isButton:
                    Button1.delete_button(screen, BACK_SCREEN)
                    del Button1
                    isButton = False

            textClients, textClientsRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "# of Clients : "+ str(serClients), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/5)
            pygame.draw.rect(screen, BACK_SCREEN, textClientsRect)
            screen.blit(textClients, textClientsRect)

            pygame.display.update()

        serverGame.main(screen, self.serObj.clients)
