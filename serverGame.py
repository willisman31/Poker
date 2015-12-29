import sys, pygame, mygui, serverThread, serverGame, time, json, copy
from pygame.locals import *
from constants import *
from deck import *
from player import *

class ServerGame:
    def __init__(self,clientSockets,screen):
        self.clientSockets = clientSockets
        self.screen = screen

    #one match = several games, one game = 4 rounds
    def update_game(self, receivedBetValue):
        if receivedBetValue < 0:
            self.numberOfUnfoldedPlayers -= 1
            self.players[self.turn].do_fold()
            #self.players[self.turn].pot = 0
        else:
            self.players[self.turn].bet(receivedBetValue)
            self.roundPot += receivedBetValue
            if self.players[self.turn].currentRoundBet > self.currentRoundBet:
                 self.currentRoundBet = self.players[self.turn].currentRoundBet
                 self.lastRaisedPlayer = self.turn


    def init_round(self):
        for i in range(self.numberOfPlayers):
            self.players[i].currentRoundBet = 0

        if self.infoFlag == 0:
            self.currentRoundBet = self.bigBlind

            temp1 = (self.start + 1)%self.numberOfPlayers
            while self.players[temp1].isActive == False:
                temp1 = (temp1 + 1)%self.numberOfPlayers

            self.players[self.start].bet(self.smallBlind)
            self.players[temp1].bet(self.bigBlind)

            temp2 = (temp1 + 1)%self.numberOfPlayers
            while self.players[temp2].isActive == False:
                temp2 = (temp2 + 1)%self.numberOfPlayers
            self.turn = temp2

            self.roundPot = self.players[self.start].currentRoundBet + self.players[temp1].currentRoundBet
        else:
            self.currentRoundBet = 0
            self.roundPot = 0
            self.turn = self.start

        self.lastRaisedPlayer = self.turn


        self.toCallAmount = self.currentRoundBet - self.players[self.serverTurn].currentRoundBet
        if not self.initGuiFlag:
            self.initGuiFlag = True
            self.gui_main(self.screen)



    def start_round(self):
        self.init_round()

        if self.numberOfUnfoldedPlayers <= 1:
            return

#        self.gui_main(self.screen)
#        self.update_gui(self.screen)

        while True:
            self.toCallAmount = self.currentRoundBet - self.players[self.serverTurn].currentRoundBet
            self.after_move(self.screen,self.butList,self.butStr,self.butXY,self.cardDrawn,self.exTurn,self.exPot)

            if (not self.players[self.turn].fold) and self.players[self.turn].money != 0 and self.players[self.turn].isActive:
                self.broadcast()
                if self.turn == self.serverTurn:
                    recievedBetValue = self.server_move(self.screen,self.butList,self.butStr,self.butXY,self.cardDrawn)    #server_move()
                else:
                    self.client_move(self.screen,self.butList,self.butStr,self.butXY,self.cardDrawn)
                    recievedBetValue = int(self.clientSockets[self.turn].recv(1024))     # wait for client to move
                self.update_game(recievedBetValue)

            self.exTurn = self.turn
            self.exPot = self.pot

            self.turn = (self.turn+1)%self.numberOfPlayers

            #self.after_move(self.screen,self.butList,self.butStr,self.butXY,self.cardDrawn)

            if self.turn == self.lastRaisedPlayer or self.numberOfUnfoldedPlayers <= 1:
                break
        self.fin_round()
        #self.broadcast()


    def fin_round(self):
        self.pot += self.roundPot
        self.roundPot = 0
        for i in range(0, self.numberOfPlayers):
            self.players[i].currentRoundBet = 0


    def init_hand(self):
        self.deck = Deck()
        self.tableCards = []
        self.smallBlind = 10
        self.bigBlind = self.smallBlind * 2
        self.handWinner = -1
        self.numberOfUnfoldedPlayers = self.numberOfActivePlayers
        self.pot = 0
        self.winCards = (self.deck.pop(),self.deck.pop())
        #Initializing cards
        self.cards = {0:[]}
        i = 0
        for cSock in self.clientSockets:
            self.cards[cSock] = (self.deck.pop(),self.deck.pop())
            self.cards[i] = self.cards[cSock]
            i += 1
        self.cards[self.serverTurn] = (self.deck.pop(),self.deck.pop()) #Server Cards

        self.myCards = self.cards[self.serverTurn]

        for i in range(self.numberOfPlayers):
            self.players[i].pot = 0
            self.players[i].fold = False

        self.initGuiFlag = False


    def start_hand(self):
        self.init_hand()

        self.infoFlag = 0          # round 0
        self.start_round()

        self.tableCards.append(self.deck.pop())
        self.tableCards.append(self.deck.pop())
        self.tableCards.append(self.deck.pop())
        self.infoFlag = 1         # round 1
        self.start_round()

        self.tableCards.append(self.deck.pop())
        self.infoFlag = 2         # round 2
        self.start_round()

        self.tableCards.append(self.deck.pop())
        self.infoFlag = 3         # round 3
        self.start_round()

        self.infoFlag = 10        # Result 10
        print "Hand completed"
        self.fin_hand()


    def fin_hand(self):
        # Decrese numberOfActivePlayers and remove from activePlayers
        for i in self.activePlayers:
            if self.players[i].money == 0:
                self.players[i].isActive = False
                self.numberOfActivePlayers -= 1
                self.activePlayers.remove(i)
        # Hand result
        self.hand_result()
        # increment start
        self.start = (self.start + 1)%self.numberOfPlayers
        while self.players[self.start].isActive == False:
            self.start = (self.start + 1)%self.numberOfPlayers


        self.broadcast()          # Final broadcast, broadcast result
        self.after_move(self.screen,self.butList,self.butStr,self.butXY,self.cardDrawn,self.exTurn,self.exPot)

    def init_game(self):

        self.initGuiFlag = False

        self.numberOfPlayers = len(self.clientSockets) + 1
        self.numberOfActivePlayers = self.numberOfPlayers
        self.gameWinner = -1
        self.serverTurn = self.numberOfPlayers - 1
        self.start = 0
        self.myTurn = self.serverTurn


        #Initializing cards and player
        self.players = {0:[]}
        for i in range(self.numberOfPlayers):
            self.players[i] = Player(i,"client "+str(i))
        self.players[self.serverTurn].name = "Server"

        # List of ids of active players
        self.activePlayers = range(self.numberOfActivePlayers)


    def start_game(self):
        self.init_game()

        #multiple hands : game > hand > round
        while self.numberOfActivePlayers > 1:
            self.start_hand()

        self.fin_game()

    def fin_game(self):
        pass

    def broadcast(self):   # infoFlag, client's cards, myTurn, players, tablecards, turn, numberOfPlayers, pot, toCallAmount
        i=0
        for cSock in self.clientSockets:
            msgPlayerCards = json.dumps(self.cards[cSock])
            msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
            msgTableCards = json.dumps(self.tableCards)

            toCallAmount = self.currentRoundBet - self.players[i].currentRoundBet
            things = (self.turn, self.numberOfPlayers, self.pot, toCallAmount, self.handWinner, self.infoFlag, self.winCards)
            msgThings = json.dumps(things)

            completeMessage = msgPlayerCards+"::"+str(i)+"::"+msgPlayers+"::"+msgTableCards+"::"+msgThings
            i+=1

            cSock.send(completeMessage)
            print "Size of message sent : "+ str(sys.getsizeof(completeMessage)) +" bytes!"

    def hand_result(self):
        self.handWinner = self.serverTurn     # Server is the winner
        self.players[self.handWinner].money += self.pot
        self.pot = 0
        self.winCards = self.cards[self.serverTurn]
        # self.broadcast()

    #GUI should be updated at the time broadcast
    # def broadcast(self):    #players, tablecards, turn, numberOfPlayers, pot, toCallAmount = currentRoundBet - currentRoundPlayerBet
    #
    #     for cSock in self.clientSockets:
    #         msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
    #         msgTableCards = json.dumps(self.tableCards)
    #         things = (self.turn, self.numberOfPlayers, self.pot)
    #         msgThings = json.dumps(things)
    #
    #         completeMessage = msgPlayerCards+"::"+str(i)+"::"+msgPlayers+"::"+msgTableCards+"::"+msgThings
    #         cSock.send(completeMessage)
    #         print sys.getsizeof(completeMessage)
    #         # cSock.send(msgPlayers)
    #         # cSock.send(msgTableCards)
    #         # cSock.send(msgThings)





    ############################
    # Code for GUI starts here #
    ############################

    def after_move(self,screen,butList,butStr,butXY,cardDrawn,exTurn,exPot):

        # exTurn = self.turn
        # exPot = self.pot

        self.update_MONEY()

        self.draw_boy(screen, self.turn, self.myTurn, self.turn)
        self.draw_boy_box(screen, self.turn)

        self.draw_boy(screen, exTurn, self.myTurn, self.turn)
        self.draw_boy_box(screen, exTurn)

        if self.infoFlag == 0:
            #Draw init cards
            if not cardDrawn[0]:
                txtCard1, txtCard1Rect1 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.myCards[0][0])+","+str(self.myCards[0][1])+")", WHITE, None, 50, 420 )
                txtCard2, txtCard2Rect2 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.myCards[1][0])+","+str(self.myCards[1][1])+")", WHITE, None,120 ,420  )
                screen.blit(txtCard1, txtCard1Rect1)
                screen.blit(txtCard2, txtCard2Rect2)
                cardDrawn[0] = True

        if self.infoFlag == 1:
            if not cardDrawn[1]:
                tblCard1, tblCard1Rect1 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.tableCards[0][0])+","+str(self.tableCards[0][1])+")", WHITE, None, 140+20, 200 )
                tblCard2, tblCard2Rect2 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.tableCards[1][0])+","+str(self.tableCards[1][1])+")", WHITE, None,210+20 ,200  )
                tblCard3, tblCard3Rect3 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.tableCards[2][0])+","+str(self.tableCards[2][1])+")", WHITE, None,280 +20,200  )
                screen.blit(tblCard1, tblCard1Rect1)
                screen.blit(tblCard2, tblCard2Rect2)
                screen.blit(tblCard3, tblCard3Rect3)
                cardDrawn[1] = True

        elif self.infoFlag == 2:
            if not cardDrawn[2]:
                tblCard4, tblCard4Rect4 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.tableCards[3][0])+","+str(self.tableCards[3][1])+")", WHITE, None,350 +20,200  )
                screen.blit(tblCard4, tblCard4Rect4)
                cardDrawn[2] = True
        elif self.infoFlag == 3:
            if not cardDrawn[3]:
                tblCard5, tblCard5Rect5 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.tableCards[4][0])+","+str(self.tableCards[4][1])+")", WHITE, None,420 +20,200  )
                screen.blit(tblCard5, tblCard5Rect5)
                cardDrawn[3] = True
        elif self.infoFlag == 10:
            self.end_hand()
            for i in cardDrawn:
                cardDrawn[i] = False

        #Display pot
        if self.pot>0 and self.pot-exPot>0:
            self.pot_animation(screen, self.pot)


        pygame.display.update()


    def server_move(self,screen,butList,butStr,butXY,cardDrawn):
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
                        state = self.players[self.myTurn].money
                        isSend = True

                if isSend == True:
                    return state
                    # clientSocket.send(str(state))
                    # isSend = False
                    # quit = True
                    # break


    def client_move(self,screen,butList,butStr,butXY,cardDrawn):
        screen.blit(BG1,(198,405),(198,405,244,64))

        #Create all buttons
        for o in range(4):
            butList[o].create_button_image(screen, but4, butXY[o][0], butXY[o][1], butXY[o][2], butXY[o][3], butStr[o], 16, WHITE)

        pygame.display.update()




    def update_gui(self, screen):

        state = 0
        testPot = mygui.Button()

        butList = [mygui.Button(),mygui.Button(),mygui.Button(),mygui.Button()]
        butStr = ["Check", "Fold", "Raise", "All-in"]
        butXY = [(198, 405, 120, 30),(322, 405, 120, 30),(198, 439, 120, 30),(322, 439, 120, 30),]

        self.toCallAmount = (self.currentRoundBet-self.players[self.serverTurn].currentRoundBet)
        if self.serverTurn == self.turn:
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
                        # clientSocket.send(str(state))
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
        tempTurn = (self.turn + 1)%self.numberOfPlayers
        while 1:
            if not self.players[tempTurn].fold and self.players[tempTurn].money != 0:
                break
            tempTurn = (tempTurn+1)%self.numberOfPlayers
        # self.recv(clientSocket)
        self.update_MONEY()

        #Display pot (change to include animation)
        testPot = mygui.Button()
        string = "$"+str(self.pot)
        screen.blit(PKT1, (int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80), (int(TBLWIDTH/2 - 7.5*len(string)),2*TBLHEIGHT/3-10,15*len(string), 20))
        testPot.create_button_image(screen, but6, int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80 , 15*len(string), 20, string, 12, WHITE)


        self.draw_boy(screen, tempTurn, self.serverTurn, tempTurn)
        self.draw_boy_box(screen, self.turn)

        self.draw_boy(screen, exTurn, self.serverTurn, tempTurn)
        self.draw_boy_box(screen, exTurn)


        pygame.display.update()
        return state

    def init_gui(self, screen):

        print "Inside init_gui"
        screen.blit(BG1, (0,0))
        screen.blit(PKT1, TBLTOPLEFT)

        #Putting players across the table
        for i in range(self.numberOfPlayers):
            self.draw_boy(screen,i,self.serverTurn, self.turn)

        #Putting textbuttons
        for i in range(self.numberOfPlayers):
            self.draw_boy_box(screen, i)

        #Draw init cards
        txtCard1, txtCard1Rect1 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.myCards[0][0])+","+str(self.myCards[0][1])+")", WHITE, None, 50, 420 )
        txtCard2, txtCard2Rect2 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.myCards[1][0])+","+str(self.myCards[1][1])+")", WHITE, None,120 ,420  )
        screen.blit(txtCard1, txtCard1Rect1)
        screen.blit(txtCard2, txtCard2Rect2)

        self.exTurn = self.turn
        self.exPot = 0


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

        screen.blit(PKT1, (130,int(2*TBLHEIGHT/3+70)),(50,int(2*TBLHEIGHT/3)-10,TBLWIDTH-100,30) )
        testPot = mygui.Button()
        for i in tempList:
            string = "$"+str(i)
            screen.blit(PKT1, (int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80), (int(TBLWIDTH/2 - 7.5*len(string)),2*TBLHEIGHT/3-10,15*len(string), 20))
            testPot.create_button_image(screen, but6, int(TBLWIDTH/2 - 7.5*len(string)+80), 2*TBLHEIGHT/3-10+80 , 15*len(string), 20, string, 12, WHITE)
            pygame.display.update()
            time.sleep(0.02)



    def gui_main(self, screen):

        self.turnMap = self.order_players(self.serverTurn, self.numberOfPlayers)
        self.init_box_coord()

        self.NAMES = []
        self.MONEY = []
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[i].name)
            self.MONEY.append("$"+str(self.players[i].money))

        self.init_gui(screen)

        self.testPot = mygui.Button()

        self.butList = [mygui.Button(),mygui.Button(),mygui.Button(),mygui.Button()]
        self.butStr = ["Check", "Fold", "Raise", "All-in"]
        self.butXY = [(198, 405, 120, 30),(322, 405, 120, 30),(198, 439, 120, 30),(322, 439, 120, 30)]
        self.cardDrawn = [False,False,False,False]
# pygame.display.update()
        # time.sleep(60)


    def update_MONEY(self):
        self.MONEY = []
        for i in range(self.numberOfPlayers):
            self.MONEY.append("$"+str(self.players[i].money))


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


    def end_hand(self):
        if self.infoFlag != 10:
            return
        #Do something here
        print "Hand completed!"
        print "Winner is : " + str(self.handWinner)

        #Winner box
        i = self.handWinner
        self.screen.blit(but7, self.BOYBUT[self.turnMap[i]])
        textWin, textWinRect = mygui.print_text('freesansbold.ttf', 16, "WINNER!", WHITE, None,self.BOYTXTBOX[self.turnMap[i]][0],self.BOYTXTBOX[self.turnMap[i]][2]-5 )
        self.screen.blit(textWin, textWinRect)

        #Winner cards
        winCard1, winCard1Rect1 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.winCards[0][0])+","+str(self.winCards[0][1])+")", WHITE, None, 280, 150 )
        self.screen.blit(winCard1, winCard1Rect1)
        winCard2, winCard1Rect2 = mygui.print_text('freesansbold.ttf', 16, "("+str(self.winCards[1][0])+","+str(self.winCards[1][1])+")", WHITE, None, 350, 150 )
        self.screen.blit(winCard2, winCard1Rect2)

        pygame.display.update()

        time.sleep(3)

        # #Clear table (TableCards + Pot)
        # self.screen.blit(PKT1,(80+50,180),(50,100,TBLWIDTH-100,70))
        # self.screen.blit(PKT1,(260,130),(180,50,140,40))
        #
        # #Clear winhand
        # self.screen.blit(BG1, (0,400), (0,400,150,40))
        # 
        # #Clear winBox
        # self.draw_boy_box(self.screen, self.handWinner)
        #




    ##########################
    # Code for GUI ends here #
    ##########################


def unpause_clients(clientSockets):
    for obj in clientSockets:
        obj.send("begin")


def main(screen, clientSockets):
    #clients = [1,2,3]

    unpause_clients(clientSockets)
    print "Inside serverGame file : Method main()"

    game = ServerGame(clientSockets,screen)
    game.start_game()

    time.sleep(5)
    pygame.quit()
    sys.exit()

    #init(clientSockets)
    #start_game()

if __name__ == '__main__':
    main()
