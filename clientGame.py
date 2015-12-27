import sys, pygame, mygui, serverThread, time, player, json
from pygame.locals import *
from constants import *
from operator import sub


class ClientGame:
    def __init__(self, clientSocket, screen):

        print "Inside ClientGame : init method"

        self.init_recv(clientSocket)
        self.main(clientSocket, screen)


    def init_recv(self, clientSocket):

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
        self.turn = self.things[0]
        self.numberOfPlayers = self.things[1]
        self.pot = self.things[2]


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
                screen.blit(boy1, BOYS[self.turnMap[i]])

        screen.blit(boy0, BOYS[8])

        #Putting textbuttons
        for i in range(self.numberOfPlayers):
            self.draw_boy_box(screen, i)

    def draw_boy(self, id, myTurn, turn):

        if id == myTurn and id == turn :
            screen.blit(boy3, BOYS[self.turnMap[id]])
        elif id == myTurn and id != turn :
            screen.blit(boy1, BOYS[self.turnMap[id]])
        elif id != myTurn and id == turn :
            screen.blit(boy4, BOYS[self.turnMap[id]])
        else :
            screen.blit(boy2, BOYS[self.turnMap[id]])

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


    def main(self, clientSocket, screen):

        self.turnMap = self.order_players(self.myTurn, self.numberOfPlayers)
        self.init_box_coord()

        self.init_gui(screen)
        # while 1:
        #     self.MONEY = []
        #     for o in self.players:
        #         self.MONEY.append("$"+str(self.players[str(o)].money))
        #
        #     draw_boy(self.turn, self.myTurn, self.turn)
        #     draw_boy_box(self.turn)
        #
        #     if self.myTurn == self.turn:
        #         pass
        #     else:
        #         self.recv()
        #
        #     pygame.display.update()


        pygame.display.update()
        time.sleep(5)

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

def addTuple(a, b):
    return map(sum, zip(a, b))

def subTuble(a, b):
    return map(sub, a, b)

def rem_boy(screen):
    pass
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



def test(screen):


    # players = {0:[]}
    # players[0] = player.Player(0,"Safal")
    # players[1] = player.Player(1,"Avantika")
    # players[2] = player.Player(2,"Lalit")
    # players[3] = player.Player(3,"Kariryaa")
    # players[4] = player.Player(4,"Aneja")
    # players[5] = player.Player(5,"Raman")
    # players[6] = player.Player(6,"Ankita")
    # players[7] = player.Player(7,"Bhavya")
    #
    # myTurn = 2
    # turn = 1
    # numberOfPlayers = 8
    #
    # # List of coordinates for the button below player picture
    # BOYBUT = []
    # BOYTXT = []
    # for i in range(12):
    #     BOYBUT.append((BOYS[i][0]+5, BOYS[i][1]+86))
    #     BOYTXT.append((BOYS[i][0]+50, BOYS[i][1]+94,BOYS[i][1]+108))
    #
    # NAMES = []
    # MONEY = []
    # for o in players:
    #     NAMES.append(players[o].name)
    #     MONEY.append("$"+str(players[o].money))
    #
    #
    # screen.blit(BG1, (0,0))
    # screen.blit(PKT1, TBLTOPLEFT)
    #
    # #Putting players across the table
    # temp = 0
    # for i in ORDER:
    #     temp+=1
    #     screen.blit(boy0, BOYS[i])
    #     if temp == numberOfPlayers:
    #         break
    #
    # #Putting buttons below players
    # temp = 0
    # for i in ORDER:
    #     temp+=1
    #     screen.blit(but1, BOYBUT[i])
    #     if temp == numberOfPlayers:
    #         break
    #
    # #Putting text in buttons
    # temp = 0
    # for i in ORDER:
    #     textMoney, textMoneyRect = mygui.print_text('freesansbold.ttf', 13, str(MONEY[temp]), WHITE, None,BOYTXT[i][0],BOYTXT[i][2] )
    #     textName, textNameRect = mygui.print_text('freesansbold.ttf', 13, NAMES[temp], WHITE, None,BOYTXT[i][0],BOYTXT[i][1] )
    #     screen.blit(textMoney, textMoneyRect)
    #     screen.blit(textName, textNameRect)
    #
    #     temp+=1
    #     if temp == numberOfPlayers:
    #         break






    pygame.display.update()
    time.sleep(5)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    test(screen)
