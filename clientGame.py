import sys, pygame, mygui, serverThread, time, player, json
from pygame.locals import *
from constants import *
from operator import sub


class ClientGame:
    def __init__(self, clientSocket, screen):

        print "Inside ClientGame : init method"

        self.test(screen)
        #self.init_recv(clientSocket)
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
        self.turn = int(self.things[0])
        self.numberOfPlayers = int(self.things[1])
        self.pot = int(self.things[2])

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


    def main(self, clientSocket, screen):

        self.turnMap = self.order_players(self.myTurn, self.numberOfPlayers)
        self.init_box_coord()

        self.init_gui(screen)
        while 1:
            self.MONEY = []
            for o in self.players:
                self.MONEY.append("$"+str(self.players[str(o)].money))

            self.draw_boy(screen, self.turn, self.myTurn, self.turn)
            self.draw_boy_box(screen, self.turn)


            screen.blit(but5, (198,405))
            screen.blit(but5, (322,405))
            screen.blit(but5, (198,439))
            screen.blit(but5, (322,439))
            textChk, textChkRect = mygui.print_text('freesansbold.ttf', 16, "Check", WHITE, None,258,420)
            textFold, textFoldRect = mygui.print_text('freesansbold.ttf', 16, "Fold", WHITE, None,388,420)
            textRaise, textRaiseRect = mygui.print_text('freesansbold.ttf', 16, "All In", WHITE, None,258,454)
            textAllIn, textAllInRect = mygui.print_text('freesansbold.ttf', 16, "Raise", WHITE, None,388,454)
            screen.blit(textChk, textChkRect)
            screen.blit(textFold, textFoldRect)
            screen.blit(textRaise, textRaiseRect)
            screen.blit(textAllIn, textAllInRect)
            #screen.blit(textName, textNameRect)


            #
            # if self.myTurn == self.turn:
            #     pass
            # else:
            #     self.recv()

            pygame.display.update()
            break

        pygame.display.update()
        time.sleep(60)

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

        self.myTurn = 2
        self.turn = 0
        self.numberOfPlayers = 8

        self.NAMES = []
        self.MONEY = []
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(i)].name)
            self.MONEY.append("$"+str(self.players[str(i)].money))


def addTuple(a, b):
    return map(sum, zip(a, b))

def subTuble(a, b):
    return map(sub, a, b)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    ClientGame(None, screen)
