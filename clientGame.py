import sys, pygame, mygui, serverThread, time, player, json
from pygame.locals import *
from constants import *
from operator import sub


class ClientGame:
    def __init__(self, clientSocket, screen):

        print "Inside ClientGame : init method"

        # self.test(screen)
        self.recv(clientSocket)
        self.main(clientSocket, screen)


    def recv(self, clientSocket):

        #playerCard, myTurn, Players, tblcards, things

        jsonData = clientSocket.recv(4196)
        data = jsonData.split("::")
        jsonCards = data[0]
        self.myTurn = int(data[1])
        jsonPlayers = data[2]
        jsonTblCards= data[3]
        jsonThings = data[4]

        print "Data received"
        self.myCards = json.loads(jsonCards)
        self.tableCards = json.loads(jsonTblCards)
        self.things = json.loads(jsonThings)
        self.turn = int(self.things[0])
        self.numberOfPlayers = int(self.things[1])
        self.pot = int(self.things[2])
        self.toCallAmount = int(self.things[3])
        self.winner = int(self.things[4])
        self.infoFlag = int(self.things[5])

        if self.infoFlag == 10:
            print "Eureka!!!!"

        jsonPlayers = json.loads(jsonPlayers)
        self.players = {0:[]}
        for key in jsonPlayers:
            obj = player.Player(jsonPlayers[key]['turn'], jsonPlayers[key]['name'])
            obj.fold = jsonPlayers[key]['fold']
            obj.pot = jsonPlayers[key]['pot']
            obj.money = jsonPlayers[key]['money']
            obj.currentRoundBet = jsonPlayers[key]['currentRoundBet']

            self.players[key] = obj

        self.NAMES = []
        self.MONEY = []
        for o in self.players:
            self.NAMES.append(self.players[str(o)].name)
            self.MONEY.append("$"+str(self.players[str(o)].money))


    def init_gui(self, screen):

        print "Inside init_gui"
        screen.blit(BG1, (0,0))
        screen.blit(PKT1, TBLTOPLEFT)

        #Putting players across the table
        for i in range(self.numberOfPlayers):
            self.draw_boy(screen,i,self.myTurn, self.turn)

        #Putting textbuttons
        for i in range(self.numberOfPlayers):
            self.draw_boy_box(screen, i)

    def draw_boy(self, screen, id, myTurn, turn):

        if id == myTurn and id == turn :
            screen.blit(boy2, BOYS[self.turnMap[id]])
        elif id == myTurn and id != turn :
            screen.blit(boy0, BOYS[self.turnMap[id]])
        elif id != myTurn and id == turn :
            screen.blit(boy3, BOYS[self.turnMap[id]])
        else :
            screen.blit(boy1, BOYS[self.turnMap[id]])

    def draw_boy_box(self, screen, i):
        screen.blit(but1, self.BOYBUT[self.turnMap[i]])

        textMoney, textMoneyRect = mygui.print_text('freesansbold.ttf', 13, str(self.MONEY[i]), WHITE, None,self.BOYTXTBOX[self.turnMap[i]][0],self.BOYTXTBOX[self.turnMap[i]][2] )
        textName, textNameRect = mygui.print_text('freesansbold.ttf', 13, self.NAMES[i], WHITE, None,self.BOYTXTBOX[self.turnMap[i]][0],self.BOYTXTBOX[self.turnMap[i]][1] )
        screen.blit(textMoney, textMoneyRect)
        screen.blit(textName, textNameRect)

    def init_box_coord(self):
        #List of coordinates for the button and textboxes below player picture
        self.BOYBUT = []
        self.BOYTXTBOX = [] # Tuple of 3 coordinates. Two different y coordinates and one same x coordinate for the text (x, y1, y2)
        for i in range(12):
            self.BOYBUT.append((BOYS[i][0]+5, BOYS[i][1]+86))
            self.BOYTXTBOX.append((BOYS[i][0]+50, BOYS[i][1]+94,BOYS[i][1]+108))

    def pot_animation(self, screen, num):
        tempList = []
        for i in range(20,0,-1):
            tempList.append(num/i)

        testPot = mygui.Button()
        for i in tempList:
            string = "$"+str(i)
            screen.blit(PKT1, (int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80), (int(TBLWIDTH/2 - 7.5*len(string)),2*TBLHEIGHT/3-10,15*len(string), 20))
            testPot.create_button_image(screen, but6, int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80 , 15*len(string), 20, string, 12, WHITE)
            pygame.display.update()
            time.sleep(0.02)



    def main(self, clientSocket, screen):

        self.turnMap = self.order_players(self.myTurn, self.numberOfPlayers)
        self.init_box_coord()


        self.init_gui(screen)

        testPot = mygui.Button()

        butList = [mygui.Button(),mygui.Button(),mygui.Button(),mygui.Button()]
        butStr = ["Check", "Fold", "Raise", "All-in"]
        butXY = [(198, 405, 120, 30),(322, 405, 120, 30),(198, 439, 120, 30),(322, 439, 120, 30),]

        while 1:
            if self.myTurn == self.turn:

                #Create all buttons
                for o in range(4):
                    if o==0 and self.toCallAmount != 0:
                        strCall = "Call $"+ str(self.toCallAmount)
                        butList[o].create_button_image(screen, but5, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], strCall, 16, WHITE)
                    else:
                        butList[o].create_button_image(screen, but5, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], butStr[o], 16, WHITE)

                pygame.display.update()

                butHover = [False, False, False, False]

                quit = False
                while not quit:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        #Mouse Hover handling
                        MOUSEPOS = pygame.mouse.get_pos()
                        for o in range(4):
                            if butList[o].hover(MOUSEPOS):
                                if not butHover[o]:
                                    screen.blit(BG1,(butXY[o][0],butXY[o][1]),butXY[o])
                                    if o==0 and self.toCallAmount != 0:
                                        strCall = "Call $"+ str(self.toCallAmount)
                                        butList[o].create_button_image(screen, but4, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], strCall, 16, WHITE)
                                    else:
                                        butList[o].create_button_image(screen, but4, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], butStr[o], 16, WHITE)

                                    pygame.display.update()
                                    butHover[o] = True
                            else:
                                if butHover[o]:
                                    if o==0 and self.toCallAmount != 0:
                                        strCall = "Call $"+ str(self.toCallAmount)
                                        butList[o].create_button_image(screen, but5, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], strCall, 16, WHITE)
                                    else:
                                        butList[o].create_button_image(screen, but5, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], butStr[o], 16, WHITE)

                                    pygame.display.update()
                                    butHover[o] = False

                        #Mouse click handling
                        isSend = False
                        if event.type == MOUSEBUTTONDOWN:
                            if butList[0].pressed(pygame.mouse.get_pos()):
                                state = self.toCallAmount
                                isSend = True
                            elif butList[1].pressed(pygame.mouse.get_pos()):
                                state = -1
                                isSend = True
                            elif butList[2].pressed(pygame.mouse.get_pos()):
                                state = max(self.toCallAmount,10)*2 #Change it later
                                isSend = True
                            elif butList[3].pressed(pygame.mouse.get_pos()):
                                state = self.players[str(self.myTurn)].money
                                isSend = True

                        if isSend == True:
                            clientSocket.send(str(state))
                            isSend = False
                            quit = True
                            break


            else:
                screen.blit(BG1,(198,405),(198,405,244,64))

                #Create all buttons
                for o in range(4):
                    butList[o].create_button_image(screen, but4, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], butStr[o], 16, WHITE)

                pygame.display.update()

            exTurn = self.turn
            self.recv(clientSocket)
            self.update_game()

            #Display pot (change to include animation)
            if self.pot>0:
                testPot = mygui.Button()
                string = "$"+str(self.pot)
                screen.blit(PKT1, (int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80), (int(TBLWIDTH/2 - 7.5*len(string)),2*TBLHEIGHT/3-10,15*len(string), 20))
                testPot.create_button_image(screen, but6, int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80 , 15*len(string), 20, string, 12, WHITE)

            self.draw_boy(screen, self.turn, self.myTurn, self.turn)
            self.draw_boy_box(screen, self.turn)

            self.draw_boy(screen, exTurn, self.myTurn, self.turn)
            self.draw_boy_box(screen, exTurn)

            self.end_hand()
            pygame.display.update()


        # pygame.display.update()
        # time.sleep(60)

    def update_game(self):
        self.MONEY = []
        for o in self.players:
            self.MONEY.append("$"+str(self.players[str(o)].money))

    def end_hand(self):
        if self.infoFlag != 10:
            return
        #Do something here
        print "Hand completed!!"
        print "Winner is : " + str(self.winner)



    def order_players(self, myturn, numberOfPlayers):
        order = {0:[]}
        fo = list(ORDER[:numberOfPlayers])
        fo.sort()
        while True:
            if fo[0] == 8:  #8 is the middle player for now
                break
            temp = fo[0]
            del fo[0]
            fo.append(temp)
        fu = range(0, numberOfPlayers)
        while True:
            if fu[0] == myturn:
                break
            temp = fu[0]
            del fu[0]
            fu.append(temp)
        for i in range(0, numberOfPlayers):
            order[fu[i]] = fo[i]
        return order





        #pygame.display.update()
        #time.sleep(5)

    def test(self, screen):

        self.players = {0:[]}
        self.players['0'] = player.Player(0,"Safal")
        self.players['1'] = player.Player(1,"Avantika")
        self.players['2'] = player.Player(2,"Lalit")
        self.players['3'] = player.Player(3,"Kariryaa")
        self.players['4'] = player.Player(4,"Aneja")
        self.players['5'] = player.Player(5,"Raman")
        self.players['6'] = player.Player(6,"Ankita")
        self.players['7'] = player.Player(7,"Bhavya")

        self.myTurn = 0
        self.turn = 0
        self.numberOfPlayers = 8

        self.toCallAmount = 20
        self.pot = 100

        self.NAMES = []
        self.MONEY = []
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(i)].name)
            self.MONEY.append("$"+str(self.players[str(i)].money))





if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    ClientGame(None, screen)
