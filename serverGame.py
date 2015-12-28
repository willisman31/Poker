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
    def update_game(self, recievedBetValue):
        if recievedBetValue < 0:
            self.numberOfUnfoldedPlayers -= 1
            self.players[self.turn].do_fold()
            self.players[self.turn].pot = 0
        else:
            self.players[self.turn].bet(recievedBetValue)
            self.pot += recievedBetValue
            if self.players[self.turn].currentRoundBet > self.currentRoundBet:
                 self.currentRoundBet = self.players[self.turn].currentRoundBet
                 self.lastRaisedPlayer = self.turn


    def init_one_round(self):
        for i in range(0, self.numberOfPlayers):
            self.players[i].currentRoundBet = 0

        if not self.tableCards:
            self.players[self.start].currentRoundBet = self.smallBlind
            self.players[(self.start + 1)%self.numberOfPlayers].currentRoundBet = self.bigBlind
            self.currentRoundBet = self.bigBlind
        else:
            self.currentRoundBet = 0


    def one_round(self):
        self.init_one_round()

        self.gui_main(self.screen)
        self.update_gui(self.screen)

        while True:
            if not self.players[self.turn].fold and self.players[self.turn].money != 0:
                self.broadcast()
                if self.turn == self.serverTurn:
                    recievedBetValue = self.update_gui(self.screen)    #server_move()
                else:
                    recievedBetValue = int(self.clientSockets[self.turn].recv(1024))     # wait for client to move
                    self.update_gui(self.screen)
                self.update_game(recievedBetValue)
            self.turn = (self.turn+1)%self.numberOfPlayers
            if self.turn == self.lastRaisedPlayer or self.numberOfUnfoldedPlayers <= 1:
                break
        #self.broadcast()

    def init_one_game(self):
        self.deck = Deck()
        self.cards = {0:[]}
        self.players = {0:[]}
        self.tableCards = []
        self.smallBlind = 10
        self.bigBlind = self.smallBlind * 2
        self.start = 0
        self.winner = -1

        self.numberOfPlayers = len(self.clientSockets) + 1
        self.numberOfUnfoldedPlayers = self.numberOfPlayers
        #Initializing cards and players
        i = 0
        for cSock in self.clientSockets:
            self.cards[cSock] = (self.deck.pop(),self.deck.pop())
            self.cards[i] = self.cards[cSock]
            #players[cSock] = Player(i)
            self.players[i] = Player(i)
            i += 1

        self.serverTurn = self.numberOfPlayers - 1
        self.players[self.serverTurn] = Player(self.serverTurn,"Server")
        self.cards[self.serverTurn] = (self.deck.pop(),self.deck.pop()) #Server Cards
        #self.serverPlayer = Player(serverTurn)


        self.players[self.start].bet(self.smallBlind)

        self.players[((self.start)+1)%(self.numberOfPlayers)].bet(self.bigBlind)
        self.turn = (self.start + 2)%self.numberOfPlayers
        self.pot = self.smallBlind + self.bigBlind
        self.lastRaisedPlayer = self.turn


    def one_game(self):
        self.init_one_game()
        #self.init_broadcast()

        #time.sleep(5)
        self.infoFlag = 0          # round 0
        self.one_round()

        self.tableCards.append(deck.pop())
        self.tableCards.append(deck.pop())
        self.tableCards.append(deck.pop())
        self.infoFlag = 1         # round 1
        self.one_round()

        self.tableCards.append(deck.pop())
        self.infoFlag = 2         # round 2
        self.one_round()

        self.tableCards.append(deck.pop())
        self.infoFlag = 3         # round 3
        self.one_round()

        # self.infoFlag = 4         # round 4
        # self.broadcast()          # Final broadcast for this game before result

        self.infoFlag = 10        # Result 10
        self.result()
        self.broadcast()          # Final broadcast, broadcast result

    def start_game(self):
        self.one_game()

    def broadcast(self):   # infoFlag, client's cards, myTurn, players, tablecards, turn, numberOfPlayers, pot, toCallAmount
        i=0
        for cSock in self.clientSockets:
            msgPlayerCards = json.dumps(self.cards[cSock])
            msgPlayers = json.dumps(self.players, default=lambda o: o.__dict__)
            msgTableCards = json.dumps(self.tableCards)

            toCallAmount = self.currentRoundBet - self.players[i].currentRoundBet
            things = (self.turn, self.numberOfPlayers, self.pot, toCallAmount, self.winner, self.infoFlag)
            msgThings = json.dumps(things)

            completeMessage = msgPlayerCards+"::"+str(i)+"::"+msgPlayers+"::"+msgTableCards+"::"+msgThings
            i+=1

            cSock.send(completeMessage)
            print "Size of message sent : "+ str(sys.getsizeof(completeMessage)) +" bytes!"


    def result(self):
        winner = numberOfPlayers-1      # Server is the winner
        self.players[winner].money += self.pot
        self.pot = 0
        #self.broadcast()

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

    def update_gui(self, screen):
        state = 0
        if self.serverTurn == self.turn:

            butChk = mygui.Button()
            butChk.create_button_image(screen, but5, 198, 405, 120, 30, "Check", 16, WHITE)
            butFold = mygui.Button()
            butFold.create_button_image(screen, but5, 322, 405, 120, 30, "Fold", 16, WHITE)
            butRaise = mygui.Button()
            butRaise.create_button_image(screen, but5, 198, 439, 120, 30, "Raise", 16, WHITE)
            butAllIn = mygui.Button()
            butAllIn.create_button_image(screen, but5, 322, 439, 120, 30, "All-in", 16, WHITE)

            pygame.display.update()

            quit = False
            while not quit:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    isSend = False
                    if event.type == MOUSEBUTTONDOWN:
                        if butChk.pressed(pygame.mouse.get_pos()):
                            state = 0
                            isSend = True
                        elif butFold.pressed(pygame.mouse.get_pos()):
                            state = -1
                            isSend = True
                        elif butRaise.pressed(pygame.mouse.get_pos()):
                            state = 100 #Change it later
                            isSend = True
                        elif butAllIn.pressed(pygame.mouse.get_pos()):
                            state = self.MONEY[self.myTurn]
                            isSend = True

                    if isSend == True:
                        # clientSocket.send(str(state))
                        isSend = False
                        quit = True
                        break


        else:
             screen.blit(BG1,(198,405),(198,405,244,64))

             butChk = mygui.Button()
             butChk.create_button_image(screen, but4, 198, 405, 120, 30, "Check", 16, WHITE)
             butFold = mygui.Button()
             butFold.create_button_image(screen, but4, 322, 405, 120, 30, "Fold", 16, WHITE)
             butRaise = mygui.Button()
             butRaise.create_button_image(screen, but4, 198, 439, 120, 30, "Raise", 16, WHITE)
             butAllIn = mygui.Button()
             butAllIn.create_button_image(screen, but4, 322, 439, 120, 30, "All-in", 16, WHITE)

             pygame.display.update()

        exTurn = self.turn
        # self.recv(clientSocket)
        self.update_MONEY()

        self.draw_boy(screen, self.turn, self.serverTurn, self.turn)
        self.draw_boy_box(screen, self.turn)

        pygame.display.update()
        return state

    def init_gui(self, screen):

        print "Inside init_gui of serverGame"
        screen.blit(BG1, (0,0))
        screen.blit(PKT1, TBLTOPLEFT)

        #Putting players across the table
        for i in range(self.numberOfPlayers):
                screen.blit(boy1, BOYS[self.turnMap[i]])

        screen.blit(boy0, BOYS[8])

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


    def gui_main(self, screen):

        self.turnMap = self.order_players(self.serverTurn, self.numberOfPlayers)
        self.init_box_coord()

        self.NAMES = []
        self.MONEY = []
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[i].name)
            self.MONEY.append("$"+str(self.players[i].money))

        self.init_gui(screen)
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
    screen.fill(BACK_SCREEN)
    pygame.display.update()

    game = ServerGame(clientSockets,screen)
    game.start_game()

    time.sleep(5)
    pygame.quit()
    sys.exit()

    #init(clientSockets)
    #start_game()

if __name__ == '__main__':
    main()
