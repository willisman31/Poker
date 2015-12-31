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
        self.winners = data[5]

        print "Data received"
        self.myCards = json.loads(jsonCards)
        self.tableCards = json.loads(jsonTblCards)
        self.winners = json.loads(self.winners)
        self.things = json.loads(jsonThings)
        self.turn = int(self.things[0])
        self.numberOfPlayers = int(self.things[1])
        self.pot = int(self.things[2])
        self.toCallAmount = int(self.things[3])
        self.infoFlag = int(self.things[4])
        self.winCards = self.things[5]
        self.maxBet = self.things[6]
        self.resultRating = int(self.things[7])

        jsonPlayers = json.loads(jsonPlayers)
        self.players = {0:[]}
        for key in jsonPlayers:
            obj = player.Player(jsonPlayers[key]['turn'], jsonPlayers[key]['name'])
            obj.fold = jsonPlayers[key]['fold']
            obj.pot = jsonPlayers[key]['pot']
            obj.money = jsonPlayers[key]['money']
            obj.currentRoundBet = jsonPlayers[key]['currentRoundBet']
            obj.isActive = jsonPlayers[key]['isActive']

            self.players[key] = obj

        self.NAMES = []
        self.MONEY = []
        self.ROUNDBET = []
        for o in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(o)].name)
            self.MONEY.append("$"+str(self.players[str(o)].money))
            self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))


    def load_cards(self):
        self.cardHearts = []
        self.cardDiamonds = []
        self.cardClubs = []
        self.cardSpades = []
        self.cardHeartsB = []
        self.cardDiamondsB = []
        self.cardClubsB = []
        self.cardSpadesB = []

        for j in range(4):
            for i in range(13):
                card1 = pygame.Surface((CARDLENIMG,CARDWIDIMG), pygame.SRCALPHA, 32)   #Card size 43 * 62
                card1.blit(CARDS, (0, 0), (i*44, j*63, CARDLENIMG, CARDWIDIMG))

                if j == 0:
                    self.cardHeartsB.append(card1)
                    self.cardHearts.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))     #Size is 36 * 49
                elif j == 1:
                    self.cardDiamondsB.append(card1)
                    self.cardDiamonds.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))
                elif j == 2:
                    self.cardClubsB.append(card1)
                    self.cardClubs.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))
                else :
                    self.cardSpadesB.append(card1)
                    self.cardSpades.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))


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

        #Putting betButtons
        for i in range(self.numberOfPlayers):
            self.draw_boy_bet(screen, i)


        #Draw init cards
        self.draw_big_card(screen, self.myCards[0],(50,410))
        self.draw_big_card(screen, self.myCards[1],(95,410))


    def draw_big_card(self, screen, card, (posX, posY)):
        if card[0] == 'C':
            if card[1] == 14:
                screen.blit(self.cardClubsB[0],(posX,posY))
            else :
                screen.blit(self.cardClubsB[card[1]-1],(posX,posY))

        elif card[0] == 'H':
            if card[1] == 14:
                screen.blit(self.cardHeartsB[0],(posX,posY))
            else :
                screen.blit(self.cardHeartsB[card[1]-1],(posX,posY))

        elif card[0] == 'D':
            if card[1] == 14:
                screen.blit(self.cardDiamondsB[0],(posX,posY))
            else :
                screen.blit(self.cardDiamondsB[card[1]-1],(posX,posY))

        elif card[0] == 'S':
            if card[1] == 14:
                screen.blit(self.cardSpadesB[0],(posX,posY))
            else :
                screen.blit(self.cardSpadesB[card[1]-1],(posX,posY))

        else : print "Wrong suit! Check your card. :- ",card


    def draw_card(self, screen, card, (posX, posY)):
        if card[0] == 'C':
            if card[1] == 14:
                screen.blit(self.cardClubs[0],(posX,posY))
            else :
                screen.blit(self.cardClubs[card[1]-1],(posX,posY))

        elif card[0] == 'H':
            if card[1] == 14:
                screen.blit(self.cardHearts[0],(posX,posY))
            else :
                screen.blit(self.cardHearts[card[1]-1],(posX,posY))

        elif card[0] == 'D':
            if card[1] == 14:
                screen.blit(self.cardDiamonds[0],(posX,posY))
            else :
                screen.blit(self.cardDiamonds[card[1]-1],(posX,posY))

        elif card[0] == 'S':
            if card[1] == 14:
                screen.blit(self.cardSpades[0],(posX,posY))
            else :
                screen.blit(self.cardSpades[card[1]-1],(posX,posY))

        else : print "Wrong suit! Check your card. :- ",card




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

    def draw_boy_bet(self, screen, i):
        obj = mygui.Button()
        screen.blit(PKT1,(self.BUTROUNDBET[self.turnMap[i]][0], self.BUTROUNDBET[self.turnMap[i]][1]),(self.BUTROUNDBET[self.turnMap[i]][0]-80, self.BUTROUNDBET[self.turnMap[i]][1]-80,20+6*11,20))
        if self.ROUNDBET[i]!="$0":
            obj.create_button_image(screen, but8, self.BUTROUNDBET[self.turnMap[i]][0], self.BUTROUNDBET[self.turnMap[i]][1] , 20+6*len(self.ROUNDBET[i]), 15, self.ROUNDBET[i], 12, WHITE)


    def init_box_coord(self):
        #List of coordinates for the button and textboxes below player picture
        self.BOYBUT = []
        self.BOYTXTBOX = [] # Tuple of 3 coordinates. Two different y coordinates and one same x coordinate for the text (x, y1, y2)
        self.BUTROUNDBET = [(115,150),(175,120),(275,120),(375,120),(445,150),(455,200),(425,235),(175,265),(275,265),(375,265),(135,235),(105,200)]
        for i in range(12):
            self.BOYBUT.append((BOYS[i][0]+5, BOYS[i][1]+86))
            self.BOYTXTBOX.append((BOYS[i][0]+50, BOYS[i][1]+94,BOYS[i][1]+108))

    def pot_animation(self, screen, num):
        tempList = []
        for i in range(20,0,-1):
            tempList.append(num/i)

        screen.blit(PKT1, (250,int(2*TBLHEIGHT/3+80)),(170,int(2*TBLHEIGHT/3),120,20) )
        testPot = mygui.Button()
        for i in tempList:
            string = "$"+str(i)
            screen.blit(PKT1, (int(TBLWIDTH/2 - (10+3.5*len(string))+80), 2*TBLHEIGHT/3+80), (int(TBLWIDTH/2 - (10+3.5*len(string))),2*TBLHEIGHT/3,20+7*len(string), 20))
            testPot.create_button_image(screen, but6, int(TBLWIDTH/2 - (10+3.5*len(string)))+80, 2*TBLHEIGHT/3+80 , 20 + 7*len(string), 20, string, 13, WHITE)
            pygame.display.update()
            time.sleep(0.02)



    def main(self, clientSocket, screen):

        self.turnMap = self.order_players(self.myTurn, self.numberOfPlayers)

        self.load_cards()
        self.init_box_coord()

        self.init_gui(screen)

        testPot = mygui.Button()

        butList = [mygui.Button(),mygui.Button(),mygui.Button(),mygui.Button()]
        butStr = ["Check", "Fold", "All-in", "Raise"]
        butXY = [(198, 405, 120, 30),(322, 405, 120, 30),(198, 439, 120, 30),(322, 439, 120, 30)]
        cardDrawn = [False,False,False,False]

        obj = mygui.Slider(screen,(450,450),(self.toCallAmount,100))

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

                #Create raise slider
                obj = mygui.Slider(screen,(450,450),(self.toCallAmount,self.maxBet))

                quit = False
                while not quit:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        #Slider event handle
                        obj.event_slider(event, pygame.mouse.get_pos())
                        #Updating the slider values
                        obj.slider_update(screen)

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
                                state = self.maxBet
                                isSend = True
                            elif butList[3].pressed(pygame.mouse.get_pos()):
                                state = obj.getValue()
                                # print "Raised : ",type(state),state
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

                #Remove slider
                obj.slider_remove(screen)

                pygame.display.update()

            exTurn = self.turn
            exPot = self.pot

            self.recv(clientSocket)
            self.update_game()


            self.draw_boy(screen, self.turn, self.myTurn, self.turn)
            self.draw_boy_box(screen, self.turn)

            self.draw_boy(screen, exTurn, self.myTurn, self.turn)
            self.draw_boy_box(screen, exTurn)

            for i in range(self.numberOfPlayers):
                self.draw_boy_bet(screen, i)

            if self.infoFlag == 0:
                #Draw init cards
                if not cardDrawn[0]:
                    self.draw_big_card(screen, self.myCards[0],(50,410))
                    self.draw_big_card(screen, self.myCards[1],(95,410))
                    cardDrawn[0] = True

            if self.infoFlag == 1:
                 if not cardDrawn[1]:
                    self.draw_card(screen, self.tableCards[0],(220,180))
                    self.draw_card(screen, self.tableCards[1],(260,180))
                    self.draw_card(screen, self.tableCards[2],(300,180))
                    cardDrawn[1] = True

            elif self.infoFlag == 2:
                 if not cardDrawn[2]:
                    self.draw_card(screen, self.tableCards[3],(340,180))
                    cardDrawn[2] = True
            elif self.infoFlag == 3:
                 if not cardDrawn[3]:
                    self.draw_card(screen, self.tableCards[4],(380,180))
                    cardDrawn[3] = True
            elif self.infoFlag == 10:
                self.end_hand(screen, clientSocket)
                for i in range(4):
                    cardDrawn[i] = False

            #Display pot
            if self.pot>0 and self.pot-exPot>0:
                self.pot_animation(screen, self.pot)

            pygame.display.update()



    def update_game(self):
        self.MONEY = []
        self.ROUNDBET= []
        for o in range(self.numberOfPlayers):
            self.MONEY.append("$"+str(self.players[str(o)].money))
            self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))

    def end_hand(self,screen, clientSocket):
        if self.infoFlag != 10:
            return
        #Do something here
        print "Hand completed!"
        print "Winner is : " + str(self.winners)

        #Winner box
        for i in self.winners:
            screen.blit(but7, self.BOYBUT[self.turnMap[i]])
            textWin, textWinRect = mygui.print_text('freesansbold.ttf', 16, "WINNER!", WHITE, None,self.BOYTXTBOX[self.turnMap[i]][0],self.BOYTXTBOX[self.turnMap[i]][2]-5 )
            screen.blit(textWin, textWinRect)

        #Winner cards
        self.draw_card(screen, self.winCards[0],(280,125))
        self.draw_card(screen, self.winCards[1],(320,125))

        #Result
        string = self.result_string(self.resultRating)
        resBut = mygui.Button()
        resBut.create_button_image(screen, but9, int(TBLWIDTH/2 - (3.5*len(string)))+80, 113 , 7*len(string), 12, string, 11, WHITE)

        pygame.display.update()

        time.sleep(4)

        self.recv(clientSocket)
        self.init_gui(screen)

    def result_string(self, rating):
        mapping = {1 : "High Card", 2: "One Pair", 3: "Two Pair", 4: "Three of a kind", 5: "Straight", 6: "Flush",
                    7: "Full House", 8: "Four of a kind", 9: "Straight Flush", 10: "Royal Flush"}

        return mapping[rating]

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
        self.players['8'] = player.Player(8,"Bhavya")
        self.players['9'] = player.Player(9,"Bhavya")
        self.players['10'] = player.Player(10,"Bhavya")
        self.players['11'] = player.Player(11,"Bhavya")
        self.players['12'] = player.Player(12,"Bhavya")

        self.players['0'].currentRoundBet = 10
        self.players['1'].currentRoundBet = 20

        self.myTurn = 3
        self.turn = 2
        self.numberOfPlayers = 12

        self.winner = 1
        self.winCards = (('H',2),('C',9))
        self.toCallAmount = 20
        self.pot = 100
        self.myCards = (('C',5),('H',7))
        self.tableCards = [('H',9),('D',2),('C',12),('S',7),('H',11)]

        self.infoFlag = 0
        self.NAMES = []
        self.MONEY = []
        self.ROUNDBET=[]
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(i)].name)
            self.MONEY.append("$"+str(self.players[str(i)].money))
            self.ROUNDBET.append("$"+str(self.players[str(i)].currentRoundBet))





if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    ClientGame(None, screen)
